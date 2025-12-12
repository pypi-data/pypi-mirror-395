from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from wd360 import __version__
from wd360.config.models import (
  dump_sample_config,
  dump_sample_function_app_config,
  load_config,
  load_function_app_config,
)
from wd360.modules.azure_vm_ai_host.builder import write_arm_template, write_arm_templates
from wd360.modules.azure_vm_ai_host.naming import vm_name
from wd360.modules.azure_function_app_ai_host.builder import write_arm_template as write_function_app_template
from wd360.modules.azure_function_app_ai_host.naming import function_app_name

app = typer.Typer(help="Watchdog360 CLI for standardized Azure AI infra templates.")


@app.callback()
def main(
  version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show version and exit.",
    is_eager=True,
  ),
) -> None:
  """Top-level entrypoint callback."""
  if version:
    typer.echo(f"wd360 {__version__}")
    raise typer.Exit()


azure_vm_app = typer.Typer(help="Azure VM AI host module commands.")
app.add_typer(azure_vm_app, name="azure-vm")


@azure_vm_app.command("init")
def azure_vm_init(
  config_path: Path = typer.Option(
    Path("wd360.azure-vm.yaml"),
    "--config",
    "-c",
    help="Path where the config file will be created.",
  ),
) -> None:
  """
  Scaffold a starter configuration file for Azure VM AI host stack.
  """
  if config_path.exists():
    typer.echo(f"Config file already exists: {config_path}")
    raise typer.Exit(code=1)

  dump_sample_config(config_path)
  # Load the config to show computed values
  cfg = load_config(config_path)
  computed_vm_name = vm_name(cfg)
  typer.echo(f"✓ Sample config written to {config_path}")
  typer.echo(f"✓ Resource Group: {cfg.resource_group}")
  typer.echo(f"✓ VM name will be: {computed_vm_name}")
  typer.echo(f"✓ Strong password has been auto-generated (see config file)")
  typer.echo(f"✓ Network CIDRs have been auto-generated (see config file)")


@azure_vm_app.command("plan")
def azure_vm_plan(
  config_path: Path = typer.Option(
    Path("wd360.azure-vm.yaml"),
    "--config",
    "-c",
    help="Path to the Azure VM config file.",
  ),
  output_path: Path = typer.Option(
    Path("arm-azure-vm-ai.json"),
    "--output",
    "-o",
    help="Path where the generated main ARM template JSON will be written.",
  ),
) -> None:
  """
  Validate config and generate ARM templates for the Azure VM AI host stack.
  Generates two templates: main infrastructure and flow logs.
  """
  cfg = load_config(config_path)
  main_template_path = output_path
  flow_logs_template_path = output_path.parent / f"{output_path.stem}-flowlogs.json"
  
  write_arm_templates(cfg, main_template_path, flow_logs_template_path)
  typer.echo(f"✓ Main ARM template written to {main_template_path}")
  typer.echo(f"✓ Flow logs ARM template written to {flow_logs_template_path}")


@azure_vm_app.command("validate")
def azure_vm_validate(
  config_path: Path = typer.Option(
    Path("wd360.azure-vm.yaml"),
    "--config",
    "-c",
    help="Path to the Azure VM config file.",
  ),
) -> None:
  """
  Validate the Azure VM AI host configuration file.
  """
  cfg = load_config(config_path)
  # If we get here, validation passed.
  computed_vm_name = vm_name(cfg)
  typer.echo("✓ Config is valid.")
  typer.echo(f"  Project: {cfg.project}")
  typer.echo(f"  Environment: {cfg.environment}")
  typer.echo(f"  Location: {cfg.location}")
  typer.echo(f"  Resource Group: {cfg.resource_group}")
  typer.echo(f"  VM name: {computed_vm_name}")
  typer.echo(f"  VM size: {cfg.vm.size}")
  typer.echo(f"  OS: {cfg.vm.os}")
  if cfg.network:
    typer.echo(f"  VNet CIDR: {cfg.network.vnet_cidr}")
    typer.echo(f"  Subnet CIDR: {cfg.network.subnet_cidr}")
  else:
    typer.echo(f"  Network: Auto-generated (will be computed during plan)")


@azure_vm_app.command("deploy")
def azure_vm_deploy(
  config_path: Path = typer.Option(
    Path("wd360.azure-vm.yaml"),
    "--config",
    "-c",
    help="Path to the Azure VM config file.",
  ),
  resource_group: Optional[str] = typer.Option(
    None,
    "--resource-group",
    "-g",
    help="Azure resource group name (overrides config file value).",
  ),
  template_path: Optional[Path] = typer.Option(
    None,
    "--template",
    "-t",
    help="Path to ARM template JSON (will be generated if not provided).",
  ),
  subscription_id: Optional[str] = typer.Option(
    None,
    "--subscription",
    "-s",
    help="Azure subscription ID (uses default subscription if not provided).",
  ),
  deployment_name: Optional[str] = typer.Option(
    None,
    "--deployment-name",
    "-n",
    help="Deployment name (auto-generated if not provided).",
  ),
) -> None:
  """
  Deploy the Azure VM AI host stack using the generated ARM template.

  This command will:
  1. Validate the config
  2. Generate ARM template (if not provided)
  3. Deploy using 'az deployment group create'

  Requires Azure CLI to be installed and authenticated.
  """
  # Load and validate config
  cfg = load_config(config_path)
  computed_vm_name = vm_name(cfg)

  # Use resource group from config unless overridden
  rg_name = resource_group or cfg.resource_group

  # Generate templates if not provided
  if template_path is None:
    main_template_path = Path("arm-azure-vm-ai.json")
    flow_logs_template_path = Path("arm-azure-vm-ai-flowlogs.json")
    typer.echo(f"Generating ARM templates...")
    write_arm_templates(cfg, main_template_path, flow_logs_template_path)
    typer.echo(f"✓ Main template: {main_template_path}")
    typer.echo(f"✓ Flow logs template: {flow_logs_template_path}")
  else:
    # If template path provided, assume it's the main template
    main_template_path = template_path
    flow_logs_template_path = template_path.parent / f"{template_path.stem}-flowlogs.json"
    if not flow_logs_template_path.exists():
      typer.echo(f"Warning: Flow logs template not found: {flow_logs_template_path}")
      typer.echo("Generating flow logs template...")
      from wd360.modules.azure_vm_ai_host.builder import build_flow_logs_arm_template
      import json
      flow_logs_template = build_flow_logs_arm_template(cfg)
      flow_logs_template_path.write_text(json.dumps(flow_logs_template, indent=2), encoding="utf-8")

  if not main_template_path.exists():
    typer.echo(f"Error: Main template file not found: {main_template_path}")
    raise typer.Exit(code=1)

  # Generate deployment names if not provided
  if deployment_name is None:
    main_deployment_name = f"wd360-{cfg.project}-{cfg.environment}-main"
    flow_logs_deployment_name = f"wd360-{cfg.project}-{cfg.environment}-flowlogs"
  else:
    main_deployment_name = deployment_name
    flow_logs_deployment_name = f"{deployment_name}-flowlogs"

  typer.echo(f"\n=== Deployment Plan ===")
  typer.echo(f"Main resource group: {rg_name}")
  typer.echo(f"Network Watcher RG: {cfg.network_watcher_resource_group}")
  typer.echo(f"Location: {cfg.location}")
  typer.echo(f"VM name: {computed_vm_name}")

  use_shell = platform.system() == "Windows"
  
  def ensure_resource_group(rg_name: str, location: str) -> None:
    """Check if resource group exists, create if it doesn't."""
    typer.echo(f"\nChecking if resource group '{rg_name}' exists...")
    check_rg_cmd = ["az", "group", "show", "--name", rg_name]
    if subscription_id:
      check_rg_cmd.extend(["--subscription", subscription_id])
    
    if use_shell:
      check_rg_cmd_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in check_rg_cmd)
      check_result = subprocess.run(check_rg_cmd_str, shell=True, capture_output=True, text=True)
    else:
      check_result = subprocess.run(check_rg_cmd, shell=False, capture_output=True, text=True)
    
    if check_result.returncode != 0:
      # Resource group doesn't exist, create it
      typer.echo(f"Resource group '{rg_name}' not found. Creating it...")
      create_rg_cmd = ["az", "group", "create", "--name", rg_name, "--location", location]
      if subscription_id:
        create_rg_cmd.extend(["--subscription", subscription_id])
      
      if use_shell:
        create_rg_cmd_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in create_rg_cmd)
        create_result = subprocess.run(create_rg_cmd_str, shell=True, check=True, text=True)
      else:
        create_result = subprocess.run(create_rg_cmd, shell=False, check=True, text=True)
      
      typer.echo(f"✓ Resource group '{rg_name}' created successfully")
    else:
      typer.echo(f"✓ Resource group '{rg_name}' already exists")

  def run_deployment(
    template_path: Path,
    target_rg: str,
    deployment_name: str,
    extra_params: list[str] = None,
  ) -> None:
    """Run a single ARM template deployment."""
    cmd = [
      "az",
      "deployment",
      "group",
      "create",
      "--resource-group",
      target_rg,
      "--template-file",
      str(template_path.absolute()),
      "--parameters",
      f"location={cfg.location}",
      "--name",
      deployment_name,
    ]
    
    if extra_params:
      # Add extra parameters (format: key=value)
      for param in extra_params:
        cmd.extend(["--parameters", param])
    
    if subscription_id:
      cmd.extend(["--subscription", subscription_id])

    if use_shell:
      cmd_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in cmd)
      cmd_to_run = cmd_str
    else:
      cmd_to_run = cmd

    try:
      result = subprocess.run(
        cmd_to_run,
        check=True,
        shell=use_shell,
        text=True,
      )
      return True
    except subprocess.CalledProcessError as e:
      typer.echo(f"\n✗ Deployment failed with exit code {e.returncode}")
      if e.stdout:
        typer.echo(f"Stdout: {e.stdout}")
      if e.stderr:
        typer.echo(f"Stderr: {e.stderr}")
      raise

  # Ensure both resource groups exist
  ensure_resource_group(rg_name, cfg.location)
  # NetworkWatcherRG might already exist, but we'll try to ensure it
  ensure_resource_group(cfg.network_watcher_resource_group, cfg.location)

  # Deployment 1: Main infrastructure
  typer.echo(f"\n=== Step 1: Deploying main infrastructure ===")
  typer.echo(f"Resource group: {rg_name}")
  typer.echo(f"Template: {main_template_path}")
  typer.echo(f"Deployment name: {main_deployment_name}")
  
  run_deployment(main_template_path, rg_name, main_deployment_name)
  typer.echo(f"\n✓ Main infrastructure deployed successfully!")

  # Deployment 2: Flow logs (depends on main infrastructure)
  typer.echo(f"\n=== Step 2: Deploying flow logs ===")
  typer.echo(f"Resource group: {cfg.network_watcher_resource_group}")
  typer.echo(f"Template: {flow_logs_template_path}")
  typer.echo(f"Deployment name: {flow_logs_deployment_name}")
  
  # Pass resource group names as parameters for cross-RG references
  # Note: Using VNet flow logs (NSG flow logs are being retired)
  flow_logs_params = [
    f"vnetResourceGroup={rg_name}",
    f"storageResourceGroup={rg_name}",
    f"workspaceResourceGroup={rg_name}",
  ]
  
  run_deployment(flow_logs_template_path, cfg.network_watcher_resource_group, flow_logs_deployment_name, flow_logs_params)
  typer.echo(f"\n✓ Flow logs deployed successfully!")

  # Check if Azure CLI is available (non-blocking check)
  try:
    result = subprocess.run(
      ["az", "--version"],
      capture_output=True,
      check=True,
      timeout=5,
      shell=False,
    )
  except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
    typer.echo("Note: Could not verify Azure CLI availability, but proceeding with deployment...")
    typer.echo("(If deployment fails, ensure Azure CLI is installed and in your PATH)")

  # Both deployments completed successfully
  typer.echo("\n" + "="*60)
  typer.echo("✓ All deployments completed successfully!")
  typer.echo("="*60)
  typer.echo(f"\nNext steps:")
  typer.echo(f"  1. VM will be accessible at: {computed_vm_name}")
  typer.echo(f"  2. Check main resource group: az group show -g {rg_name}")
  typer.echo(f"  3. View main deployment: az deployment group show -g {rg_name} -n {main_deployment_name}")
  typer.echo(f"  4. View flow logs: az network watcher flow-log show -g {cfg.network_watcher_resource_group} -n NetworkWatcher_{cfg.location}")


# Function App commands
function_app_app = typer.Typer(help="Azure Function App AI host module commands.")
app.add_typer(function_app_app, name="function-app")


@function_app_app.command("init")
def function_app_init(
  config_path: Path = typer.Option(
    Path("wd360.function-app.yaml"),
    "--config",
    "-c",
    help="Path where the config file will be created.",
  ),
) -> None:
  """
  Scaffold a starter configuration file for Azure Function App AI host stack.
  """
  if config_path.exists():
    typer.echo(f"Config file already exists: {config_path}")
    raise typer.Exit(code=1)

  dump_sample_function_app_config(config_path)
  # Load the config to show computed values
  cfg = load_function_app_config(config_path)
  computed_func_name = function_app_name(cfg)
  typer.echo(f"✓ Sample config written to {config_path}")
  typer.echo(f"✓ Resource Group: {cfg.resource_group}")
  typer.echo(f"✓ Function App name will be: {computed_func_name}")
  typer.echo(f"✓ Runtime: {cfg.function_app.runtime} {cfg.function_app.runtime_version}")
  typer.echo(f"✓ AI keys can be configured in the 'function_app.ai_keys' section")


@function_app_app.command("plan")
def function_app_plan(
  config_path: Path = typer.Option(
    Path("wd360.function-app.yaml"),
    "--config",
    "-c",
    help="Path to the Azure Function App config file.",
  ),
  output_path: Path = typer.Option(
    Path("arm-azure-function-app-ai.json"),
    "--output",
    "-o",
    help="Path where the generated ARM template JSON will be written.",
  ),
) -> None:
  """
  Validate config and generate ARM template for the Azure Function App AI host stack.
  """
  cfg = load_function_app_config(config_path)
  write_function_app_template(cfg, output_path)
  typer.echo(f"✓ ARM template written to {output_path}")


@function_app_app.command("validate")
def function_app_validate(
  config_path: Path = typer.Option(
    Path("wd360.function-app.yaml"),
    "--config",
    "-c",
    help="Path to the Azure Function App config file.",
  ),
) -> None:
  """
  Validate the Azure Function App AI host configuration file.
  """
  cfg = load_function_app_config(config_path)
  computed_func_name = function_app_name(cfg)
  typer.echo("✓ Config is valid.")
  typer.echo(f"  Project: {cfg.project}")
  typer.echo(f"  Environment: {cfg.environment}")
  typer.echo(f"  Location: {cfg.location}")
  typer.echo(f"  Resource Group: {cfg.resource_group}")
  typer.echo(f"  Function App name: {computed_func_name}")
  typer.echo(f"  Runtime: {cfg.function_app.runtime} {cfg.function_app.runtime_version}")
  typer.echo(f"  SKU: {cfg.function_app.sku}")
  if cfg.function_app.ai_keys:
    typer.echo(f"  AI Keys configured: {', '.join(cfg.function_app.ai_keys.keys())}")
  else:
    typer.echo(f"  AI Keys: None configured (add to function_app.ai_keys)")


@function_app_app.command("deploy")
def function_app_deploy(
  config_path: Path = typer.Option(
    Path("wd360.function-app.yaml"),
    "--config",
    "-c",
    help="Path to the Azure Function App config file.",
  ),
  resource_group: Optional[str] = typer.Option(
    None,
    "--resource-group",
    "-g",
    help="Azure resource group name (overrides config file value).",
  ),
  template_path: Optional[Path] = typer.Option(
    None,
    "--template",
    "-t",
    help="Path to ARM template JSON (will be generated if not provided).",
  ),
  subscription_id: Optional[str] = typer.Option(
    None,
    "--subscription",
    "-s",
    help="Azure subscription ID (uses default subscription if not provided).",
  ),
  deployment_name: Optional[str] = typer.Option(
    None,
    "--deployment-name",
    "-n",
    help="Deployment name (auto-generated if not provided).",
  ),
) -> None:
  """
  Deploy the Azure Function App AI host stack using the generated ARM template.
  """
  # Load and validate config
  cfg = load_function_app_config(config_path)
  computed_func_name = function_app_name(cfg)

  # Use resource group from config unless overridden
  rg_name = resource_group or cfg.resource_group

  # Generate template if not provided
  if template_path is None:
    template_path = Path("arm-azure-function-app-ai.json")
    typer.echo(f"Generating ARM template to {template_path}...")
    write_function_app_template(cfg, template_path)
    typer.echo(f"✓ ARM template generated")

  if not template_path.exists():
    typer.echo(f"Error: Template file not found: {template_path}")
    raise typer.Exit(code=1)

  # Generate deployment name if not provided
  if deployment_name is None:
    deployment_name = f"wd360-{cfg.project}-{cfg.environment}-{computed_func_name}"

  typer.echo(f"\n=== Deployment Plan ===")
  typer.echo(f"Resource group: {rg_name}")
  typer.echo(f"Location: {cfg.location}")
  typer.echo(f"Function App name: {computed_func_name}")
  typer.echo(f"Runtime: {cfg.function_app.runtime} {cfg.function_app.runtime_version}")
  typer.echo(f"SKU: {cfg.function_app.sku}")

  use_shell = platform.system() == "Windows"

  def ensure_resource_group(rg_name: str, location: str) -> None:
    """Check if resource group exists, create if it doesn't."""
    typer.echo(f"\nChecking if resource group '{rg_name}' exists...")
    check_rg_cmd = ["az", "group", "show", "--name", rg_name]
    if subscription_id:
      check_rg_cmd.extend(["--subscription", subscription_id])

    if use_shell:
      check_rg_cmd_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in check_rg_cmd)
      check_result = subprocess.run(check_rg_cmd_str, shell=True, capture_output=True, text=True)
    else:
      check_result = subprocess.run(check_rg_cmd, shell=False, capture_output=True, text=True)

    if check_result.returncode != 0:
      typer.echo(f"Resource group '{rg_name}' not found. Creating it...")
      create_rg_cmd = ["az", "group", "create", "--name", rg_name, "--location", location]
      if subscription_id:
        create_rg_cmd.extend(["--subscription", subscription_id])

      if use_shell:
        create_rg_cmd_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in create_rg_cmd)
        create_result = subprocess.run(create_rg_cmd_str, shell=True, check=True, text=True)
      else:
        create_result = subprocess.run(create_rg_cmd, shell=False, check=True, text=True)

      typer.echo(f"✓ Resource group '{rg_name}' created successfully")
    else:
      typer.echo(f"✓ Resource group '{rg_name}' already exists")

  def run_deployment(
    template_path: Path,
    target_rg: str,
    deployment_name: str,
    extra_params: list[str] = None,
  ) -> None:
    """Run a single ARM template deployment."""
    cmd = [
      "az",
      "deployment",
      "group",
      "create",
      "--resource-group",
      target_rg,
      "--template-file",
      str(template_path.absolute()),
      "--parameters",
      f"location={cfg.location}",
      "--name",
      deployment_name,
    ]

    if extra_params:
      for param in extra_params:
        cmd.extend(["--parameters", param])

    if subscription_id:
      cmd.extend(["--subscription", subscription_id])

    if use_shell:
      cmd_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in cmd)
      cmd_to_run = cmd_str
    else:
      cmd_to_run = cmd

    try:
      result = subprocess.run(
        cmd_to_run,
        check=True,
        shell=use_shell,
        text=True,
      )
      return True
    except subprocess.CalledProcessError as e:
      typer.echo(f"\n✗ Deployment failed with exit code {e.returncode}")
      if e.stdout:
        typer.echo(f"Stdout: {e.stdout}")
      if e.stderr:
        typer.echo(f"Stderr: {e.stderr}")
      raise

  # Ensure resource group exists
  ensure_resource_group(rg_name, cfg.location)

  # Deploy Function App
  typer.echo(f"\n=== Deploying Function App ===")
  typer.echo(f"Resource group: {rg_name}")
  typer.echo(f"Template: {template_path}")
  typer.echo(f"Deployment name: {deployment_name}")

  run_deployment(template_path, rg_name, deployment_name)
  typer.echo(f"\n✓ Function App deployed successfully!")

  typer.echo("\n" + "="*60)
  typer.echo("✓ Deployment completed successfully!")
  typer.echo("="*60)
  typer.echo(f"\nNext steps:")
  typer.echo(f"  1. Function App URL: https://{computed_func_name}.azurewebsites.net")
  typer.echo(f"  2. Check resource group: az group show -g {rg_name}")
  typer.echo(f"  3. View deployment: az deployment group show -g {rg_name} -n {deployment_name}")
  typer.echo(f"  4. View app settings: az functionapp config appsettings list -g {rg_name} -n {computed_func_name}")


