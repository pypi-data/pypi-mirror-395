from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from wd360.config.models import AzureFunctionAppAiHostConfig
from wd360.modules.azure_function_app_ai_host import naming


def build_arm_template(cfg: AzureFunctionAppAiHostConfig) -> Dict[str, Any]:
  """
  Build ARM template for Azure Function App AI host stack.
  FlexConsumption requires an App Service Plan.
  """
  func_name = naming.function_app_name(cfg)
  storage_name = naming.storage_account_name(cfg)
  app_insights_name = naming.app_insights_name(cfg)
  asp_name = naming.app_service_plan_name(cfg)
  
  # Determine if we need to create a server farm or use an existing one
  use_existing_server_farm = cfg.existing_server_farm_id is not None

  # Build tags for resources
  tags = {
    "wd360_managed": "true",
    "wd360_profile": "azure_function_app_ai_host",
    "project": cfg.project,
    "environment": cfg.environment,
    "purpose": "ai_agent_host",
    **cfg.tags,  # Merge user-provided tags
  }

  # Build app settings (including AI keys)
  # Note: FlexConsumption doesn't allow FUNCTIONS_WORKER_RUNTIME, WEBSITE_CONTENTAZUREFILECONNECTIONSTRING, WEBSITE_CONTENTSHARE
  app_settings: Dict[str, str] = {
    "FUNCTIONS_EXTENSION_VERSION": "~4",
    "APPINSIGHTS_INSTRUMENTATIONKEY": f"[reference(resourceId('Microsoft.Insights/components', variables('appInsightsName'))).InstrumentationKey]",
    "APPLICATIONINSIGHTS_CONNECTION_STRING": f"[reference(resourceId('Microsoft.Insights/components', variables('appInsightsName'))).ConnectionString]",
    "AzureWebJobsStorage": f"[concat('DefaultEndpointsProtocol=https;AccountName=', variables('storageAccountName'), ';AccountKey=', listKeys(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), '2023-01-01').keys[0].value, ';EndpointSuffix=', environment().suffixes.storage)]",
  }
  
  # Only add these settings for non-FlexConsumption SKUs
  if cfg.function_app.sku != "FlexConsumption":
    app_settings["FUNCTIONS_WORKER_RUNTIME"] = cfg.function_app.runtime
    app_settings["WEBSITE_CONTENTAZUREFILECONNECTIONSTRING"] = f"[concat('DefaultEndpointsProtocol=https;AccountName=', variables('storageAccountName'), ';AccountKey=', listKeys(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), '2023-01-01').keys[0].value, ';EndpointSuffix=', environment().suffixes.storage)]"
    app_settings["WEBSITE_CONTENTSHARE"] = func_name

  # Add AI keys from config
  for key_name, key_value in cfg.function_app.ai_keys.items():
    app_settings[key_name] = key_value

  template: Dict[str, Any] = {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "location": {
        "type": "string",
        "defaultValue": cfg.location,
      },
    },
    "variables": {
      "functionAppName": func_name,
      "storageAccountName": storage_name,
      "appInsightsName": app_insights_name,
      "appServicePlanName": asp_name,
    },
    "resources": [],
  }
  
  # Create server farm - use FlexConsumption SKU if Function App is FlexConsumption
  if not use_existing_server_farm:
    if cfg.function_app.sku == "FlexConsumption":
      # FlexConsumption requires FC1/FlexConsumption SKU for the server farm
      # Match portal template structure
      server_farm_sku = {
        "Tier": "FlexConsumption",
        "Name": "FC1",
      }
      server_farm_properties = {
        "name": "[variables('appServicePlanName')]",
        "reserved": True,  # Required for Linux
        "zoneRedundant": False,
      }
      server_farm_kind = "linux"
    else:
      # Standard Consumption plan uses Y1/Dynamic
      server_farm_sku = {
        "Tier": "Dynamic",
        "Name": "Y1",
      }
      server_farm_properties = {
        "name": "[variables('appServicePlanName')]",
        "reserved": True,  # Required for Linux
      }
      server_farm_kind = "functionapp"
    
    template["resources"].append({
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2024-11-01",
      "name": "[variables('appServicePlanName')]",
      "location": "[parameters('location')]",
      "tags": tags,
      "kind": server_farm_kind,
      "sku": server_farm_sku,
      "properties": server_farm_properties,
    })
  
  # Add storage account
  template["resources"].append({
    "type": "Microsoft.Storage/storageAccounts",
    "apiVersion": "2023-01-01",
    "name": "[variables('storageAccountName')]",
    "location": "[parameters('location')]",
    "tags": tags,
    "sku": {
      "name": "Standard_LRS",
    },
    "kind": "StorageV2",
    "properties": {
      "supportsHttpsTrafficOnly": True,
    },
  })
  
  # Add Application Insights
  template["resources"].append({
    "type": "Microsoft.Insights/components",
    "apiVersion": "2020-02-02",
    "name": "[variables('appInsightsName')]",
    "location": "[parameters('location')]",
    "tags": tags,
    "kind": "web",
    "properties": {
      "Application_Type": "web",
      "Request_Source": "rest",
    },
  })
  
  # Add Function App
  # Build dependencies - ALWAYS include server farm if we're creating it
  depends_on = [
    "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]",
    "[resourceId('Microsoft.Insights/components', variables('appInsightsName'))]",
  ]
  
  # CRITICAL: Ensure server farm is created BEFORE Function App
  # Add server farm to dependsOn if we're creating it (not using existing)
  if not use_existing_server_farm:
    # Check if server farm resource exists in template
    server_farm_exists = any(
      r.get("type") == "Microsoft.Web/serverfarms" and r.get("name") == "[variables('appServicePlanName')]"
      for r in template["resources"]
    )
    if server_farm_exists:
      depends_on.append("[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]")
    else:
      # Server farm should have been added earlier - this is a safety check
      raise ValueError("Server farm resource not found in template but use_existing_server_farm is False")
  
  # Use existing server farm ID or reference the one we create
  if use_existing_server_farm:
    server_farm_id = cfg.existing_server_farm_id
  else:
    server_farm_id = "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]"
  
  template["resources"].append({
    "type": "Microsoft.Web/sites",
    "apiVersion": "2024-11-01",
    "name": "[variables('functionAppName')]",
    "location": "[parameters('location')]",
    "kind": "functionapp,linux",
    "tags": {
      **tags,
      "hidden-link: /app-insights-resource-id": "[resourceId('Microsoft.Insights/components', variables('appInsightsName'))]",
    },
    "dependsOn": depends_on,
    "properties": {
      "name": "[variables('functionAppName')]",
      "serverFarmId": server_farm_id,
      "siteConfig": {
        "linuxFxVersion": "" if cfg.function_app.sku == "FlexConsumption" else f"{cfg.function_app.runtime}|{cfg.function_app.runtime_version}",
        "appSettings": [
          {"name": k, "value": v} for k, v in app_settings.items()
        ],
        "alwaysOn": False,
        "http20Enabled": False,
        "functionAppScaleLimit": 100,
        "minimumElasticInstanceCount": 0,
        "webJobsEnabled": False,
        "clusteringEnabled": False,
      },
    },
  })
  
  # Add functionAppConfig and sku only for FlexConsumption
  func_app_resource = template["resources"][-1]  # Last resource is the Function App
  if cfg.function_app.sku == "FlexConsumption":
    func_app_resource["properties"]["functionAppConfig"] = {
      "deployment": {
        "storage": {
          "type": "blobcontainer",
          "value": f"[concat('https://', variables('storageAccountName'), '.blob.core.windows.net/app-package-', variables('functionAppName'), '-', uniqueString(resourceGroup().id))]",
          "authentication": {
            "type": "storageaccountconnectionstring",
            "storageAccountConnectionStringName": "DEPLOYMENT_STORAGE_CONNECTION_STRING",
          },
        },
      },
      "runtime": {
        "name": cfg.function_app.runtime,
        "version": cfg.function_app.runtime_version,
      },
      "scaleAndConcurrency": {
        "maximumInstanceCount": 100,
        "instanceMemoryMB": 512,
      },
      "siteUpdateStrategy": {
        "type": "Recreate",
      },
    }
    func_app_resource["properties"]["sku"] = cfg.function_app.sku
  
  # Add common properties
  func_app_resource["properties"]["httpsOnly"] = True
  func_app_resource["properties"]["clientCertEnabled"] = False
  func_app_resource["properties"]["clientCertMode"] = "Required"
  func_app_resource["properties"]["keyVaultReferenceIdentity"] = "SystemAssigned"
  func_app_resource["properties"]["publicNetworkAccess"] = "Enabled"
  
  return template


def write_arm_template(cfg: AzureFunctionAppAiHostConfig, path: Path) -> None:
  """Generate and write the ARM template to disk."""
  template = build_arm_template(cfg)
  text = json.dumps(template, indent=2)
  path.write_text(text, encoding="utf-8")

