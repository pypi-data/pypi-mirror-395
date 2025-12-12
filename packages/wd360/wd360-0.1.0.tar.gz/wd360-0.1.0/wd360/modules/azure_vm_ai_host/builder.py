from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from wd360.config.models import AzureVmAiHostConfig, auto_generate_network_cidrs
from wd360.modules.azure_vm_ai_host import naming


def build_main_arm_template(cfg: AzureVmAiHostConfig) -> Dict[str, Any]:
  """
  Build the main ARM template for infrastructure resources (VNet, NSG, Storage, Log Analytics).
  This template deploys to the main resource group.
  """
  vm_name = naming.vm_name(cfg)
  vnet_name = naming.vnet_name(cfg)
  subnet_name = naming.subnet_name(cfg)
  nsg_name = naming.nsg_name(cfg)
  storage_name = naming.storage_account_name(cfg)
  container_name = naming.flow_logs_container_name()
  law_name = naming.log_analytics_workspace_name(cfg)

  # Auto-generate network CIDRs if not provided
  if cfg.network and cfg.network.vnet_cidr and cfg.network.subnet_cidr:
    vnet_cidr = cfg.network.vnet_cidr
    subnet_cidr = cfg.network.subnet_cidr
  else:
    vnet_cidr, subnet_cidr = auto_generate_network_cidrs(cfg.project, cfg.environment)

  # Build tags for resources
  tags = {
    "wd360_managed": "true",
    "wd360_profile": "azure_vm_ai_host",
    "project": cfg.project,
    "environment": cfg.environment,
    "purpose": "ai_agent_host",
    **cfg.tags,  # Merge user-provided tags
  }

  template: Dict[str, Any] = {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "location": {
        "type": "string",
        "defaultValue": cfg.location,
      },
      "adminUsername": {
        "type": "string",
        "defaultValue": cfg.vm.admin_username,
        "metadata": {
          "description": "Admin username for the VM",
        },
      },
      "adminPassword": {
        "type": "securestring",
        "defaultValue": cfg.vm.password or "",
        "metadata": {
          "description": "Admin password for the VM (required for Windows, optional for Linux)",
        },
      },
      "sshPublicKey": {
        "type": "string",
        "defaultValue": cfg.vm.ssh_public_key or "",
        "metadata": {
          "description": "SSH public key for Linux VMs (optional if password is provided)",
        },
      },
    },
    "variables": {
      "vmName": vm_name,
      "nicName": f"{vm_name}-nic",
      "publicIpName": f"{vm_name}-pip",
      "vnetName": vnet_name,
      "subnetName": subnet_name,
      "nsgName": nsg_name,
      "storageAccountName": storage_name,
      "flowLogsContainer": container_name,
      "logAnalyticsWorkspaceName": law_name,
      "vmSize": cfg.vm.size,
      "osType": cfg.vm.os,
    },
    "resources": [
      {
        "type": "Microsoft.Network/networkSecurityGroups",
        "apiVersion": "2023-04-01",
        "name": "[variables('nsgName')]",
        "location": "[parameters('location')]",
        "tags": tags,
        "properties": {
          "securityRules": [
            {
              "name": "AllowSSH",
              "properties": {
                "priority": 1000,
                "access": "Allow",
                "direction": "Inbound",
                "destinationPortRange": "22",
                "protocol": "Tcp",
                "sourceAddressPrefix": "*",
                "sourcePortRange": "*",
                "destinationAddressPrefix": "*",
              },
            },
            {
              "name": "AllowHTTPSOutbound",
              "properties": {
                "priority": 1000,
                "access": "Allow",
                "direction": "Outbound",
                "destinationPortRange": "443",
                "protocol": "Tcp",
                "sourceAddressPrefix": "*",
                "sourcePortRange": "*",
                "destinationAddressPrefix": "*",
              },
            },
          ],
        },
      },
      {
        "type": "Microsoft.Network/virtualNetworks",
        "apiVersion": "2023-04-01",
        "name": "[variables('vnetName')]",
        "location": "[parameters('location')]",
        "tags": tags,
        "dependsOn": [
          "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgName'))]",
        ],
        "properties": {
          "addressSpace": {
            "addressPrefixes": [vnet_cidr],
          },
          "subnets": [
            {
              "name": "[variables('subnetName')]",
              "properties": {
                "addressPrefix": subnet_cidr,
                "networkSecurityGroup": {
                  "id": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgName'))]",
                },
              },
            }
          ],
        },
      },
      {
        "type": "Microsoft.Storage/storageAccounts",
        "apiVersion": "2023-01-01",
        "name": "[variables('storageAccountName')]",
        "location": "[parameters('location')]",
        "sku": {
          "name": "Standard_LRS",
        },
        "kind": "StorageV2",
        "properties": {
          "supportsHttpsTrafficOnly": True,
        },
      },
      {
        "type": "Microsoft.OperationalInsights/workspaces",
        "apiVersion": "2022-10-01",
        "name": "[variables('logAnalyticsWorkspaceName')]",
        "location": "[parameters('location')]",
        "tags": tags,
        "properties": {
          "sku": {
            "name": "PerGB2018",
          },
        },
      },
      {
        "type": "Microsoft.Network/publicIPAddresses",
        "apiVersion": "2023-04-01",
        "name": "[variables('publicIpName')]",
        "location": "[parameters('location')]",
        "tags": tags,
        "sku": {
          "name": "Basic",
          "tier": "Regional",
        },
        "properties": {
          "publicIPAllocationMethod": "Dynamic",
          "publicIPAddressVersion": "IPv4",
        },
      },
      {
        "type": "Microsoft.Network/networkInterfaces",
        "apiVersion": "2023-04-01",
        "name": "[variables('nicName')]",
        "location": "[parameters('location')]",
        "tags": tags,
        "dependsOn": [
          "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]",
          "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgName'))]",
          "[resourceId('Microsoft.Network/publicIPAddresses', variables('publicIpName'))]",
        ],
        "properties": {
          "ipConfigurations": [
            {
              "name": "ipconfig1",
              "properties": {
                "subnet": {
                  "id": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetName'))]",
                },
                "privateIPAllocationMethod": "Dynamic",
                "publicIPAddress": {
                  "id": "[resourceId('Microsoft.Network/publicIPAddresses', variables('publicIpName'))]",
                },
              },
            }
          ],
          "networkSecurityGroup": {
            "id": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgName'))]",
          },
        },
      },
      {
        "type": "Microsoft.Compute/virtualMachines",
        "apiVersion": "2023-03-01",
        "name": "[variables('vmName')]",
        "location": "[parameters('location')]",
        "tags": tags,
        "dependsOn": [
          "[resourceId('Microsoft.Network/networkInterfaces', variables('nicName'))]",
        ],
        "properties": {
          "hardwareProfile": {
            "vmSize": "[variables('vmSize')]",
          },
          "osProfile": {
            "computerName": "[variables('vmName')]",
            "adminUsername": "[parameters('adminUsername')]",
            **(
              {
                "adminPassword": "[parameters('adminPassword')]",
                "linuxConfiguration": {
                  "disablePasswordAuthentication": bool(cfg.vm.ssh_public_key),
                  **(
                    {
                      "ssh": {
                        "publicKeys": [
                          {
                            "path": "[concat('/home/', parameters('adminUsername'), '/.ssh/authorized_keys')]",
                            "keyData": "[parameters('sshPublicKey')]",
                          }
                        ],
                      }
                    }
                    if cfg.vm.ssh_public_key
                    else {}
                  ),
                },
              }
              if cfg.vm.os == "linux"
              else {
                "adminPassword": "[parameters('adminPassword')]",
                "windowsConfiguration": {
                  "enableAutomaticUpdates": True,
                },
              }
            ),
          },
          "storageProfile": {
            "imageReference": (
              {
                "publisher": "Canonical",
                "offer": "0001-com-ubuntu-server-jammy",
                "sku": "22_04-lts-gen2",
                "version": "latest",
              }
              if cfg.vm.os == "linux"
              else {
                "publisher": "MicrosoftWindowsServer",
                "offer": "WindowsServer",
                "sku": "2022-Datacenter",
                "version": "latest",
              }
            ),
            "osDisk": {
              "createOption": "FromImage",
              "managedDisk": {
                "storageAccountType": "Premium_LRS",
              },
            },
          },
          "networkProfile": {
            "networkInterfaces": [
              {
                "id": "[resourceId('Microsoft.Network/networkInterfaces', variables('nicName'))]",
              }
            ],
          },
        },
      },
    ],
  }

  return template


def build_flow_logs_arm_template(cfg: AzureVmAiHostConfig) -> Dict[str, Any]:
  """
  Build the ARM template for Virtual Network flow logs (VNet flow logs).
  Note: NSG flow logs are being retired. We use VNet flow logs instead.
  This template deploys to the NetworkWatcherRG resource group where Network Watcher exists.
  """
  vnet_name = naming.vnet_name(cfg)
  storage_name = naming.storage_account_name(cfg)
  law_name = naming.log_analytics_workspace_name(cfg)

  template: Dict[str, Any] = {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "location": {
        "type": "string",
        "defaultValue": cfg.location,
      },
      "vnetResourceGroup": {
        "type": "string",
        "defaultValue": cfg.resource_group,
        "metadata": {
          "description": "Resource group where the VNet exists",
        },
      },
      "storageResourceGroup": {
        "type": "string",
        "defaultValue": cfg.resource_group,
        "metadata": {
          "description": "Resource group where the storage account exists",
        },
      },
      "workspaceResourceGroup": {
        "type": "string",
        "defaultValue": cfg.resource_group,
        "metadata": {
          "description": "Resource group where the Log Analytics workspace exists",
        },
      },
    },
    "variables": {
      "vnetName": vnet_name,
      "storageAccountName": storage_name,
      "logAnalyticsWorkspaceName": law_name,
      "networkWatcherName": f"NetworkWatcher_{cfg.location}",
    },
    "resources": [
      {
        # Enable Virtual Network flow logs v2 + Traffic Analytics
        # Note: NSG flow logs are being retired (June 2025), so we use VNet flow logs instead
        # Network Watcher is a singleton (1 per subscription per region)
        # It exists in NetworkWatcherRG resource group
        "type": "Microsoft.Network/networkWatchers/flowLogs",
        "apiVersion": "2023-04-01",
        "name": "[concat(variables('networkWatcherName'), '/wd360-vnet-flowlog-', variables('vnetName'))]",
        "location": "[parameters('location')]",
        "properties": {
          "targetResourceId": "[concat('/subscriptions/', subscription().subscriptionId, '/resourceGroups/', parameters('vnetResourceGroup'), '/providers/Microsoft.Network/virtualNetworks/', variables('vnetName'))]",
          "storageId": "[concat('/subscriptions/', subscription().subscriptionId, '/resourceGroups/', parameters('storageResourceGroup'), '/providers/Microsoft.Storage/storageAccounts/', variables('storageAccountName'))]",
          "enabled": True,
          "format": {
            "type": "JSON",
            "version": 2,
          },
          "retentionPolicy": {
            "days": 30,
            "enabled": True,
          },
          "flowAnalyticsConfiguration": {
            "networkWatcherFlowAnalyticsConfiguration": {
              "enabled": True,
              "workspaceResourceId": "[concat('/subscriptions/', subscription().subscriptionId, '/resourceGroups/', parameters('workspaceResourceGroup'), '/providers/Microsoft.OperationalInsights/workspaces/', variables('logAnalyticsWorkspaceName'))]",
              "trafficAnalyticsInterval": 60,
            },
          },
        },
      },
    ],
  }

  return template


def write_arm_templates(cfg: AzureVmAiHostConfig, main_template_path: Path, flow_logs_template_path: Path) -> None:
  """Generate and write both ARM templates to disk."""
  main_template = build_main_arm_template(cfg)
  flow_logs_template = build_flow_logs_arm_template(cfg)
  
  main_text = json.dumps(main_template, indent=2)
  flow_logs_text = json.dumps(flow_logs_template, indent=2)
  
  main_template_path.write_text(main_text, encoding="utf-8")
  flow_logs_template_path.write_text(flow_logs_text, encoding="utf-8")


# Backward compatibility: keep old function name that writes single template
def write_arm_template(cfg: AzureVmAiHostConfig, path: Path) -> None:
  """Generate and write the main ARM template to disk (for backward compatibility)."""
  template = build_main_arm_template(cfg)
  text = json.dumps(template, indent=2)
  path.write_text(text, encoding="utf-8")


