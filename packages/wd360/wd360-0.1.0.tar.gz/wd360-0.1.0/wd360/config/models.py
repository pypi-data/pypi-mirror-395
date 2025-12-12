from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field, HttpUrl, field_validator


class VmConfig(BaseModel):
  os: str = Field(default="linux", description="Operating system: linux or windows")
  size: str = Field(description="Azure VM size, e.g. Standard_D4s_v5")
  admin_username: str = Field(description="Admin username for the VM")
  ssh_public_key: Optional[str] = Field(
    default=None,
    description="SSH public key for Linux VMs (optional, password will be used if not provided)",
  )
  password: Optional[str] = Field(
    default=None,
    description="Password for VM authentication (auto-generated if not provided)",
  )
  name_suffix: str = Field(
    default="01",
    description="Suffix for the VM name, e.g. vm-wd360-<project>-<env>-01",
  )

  @field_validator("os")
  @classmethod
  def validate_os(cls, value: str) -> str:
    value_normalized = value.lower()
    if value_normalized not in {"linux", "windows"}:
      raise ValueError("os must be either 'linux' or 'windows'")
    return value_normalized

  @field_validator("ssh_public_key", "password")
  @classmethod
  def validate_auth(cls, v: Optional[str], info):
    # Actual cross-field validation happens in parent model; this exists
    # to keep mypy and pydantic happy.
    return v


class NetworkConfig(BaseModel):
  vnet_cidr: Optional[str] = Field(
    default=None,
    description="VNet CIDR block (auto-generated if not provided, e.g. 10.10.0.0/16)",
  )
  subnet_cidr: Optional[str] = Field(
    default=None,
    description="Subnet CIDR block (auto-generated if not provided, e.g. 10.10.1.0/24)",
  )


class FunctionAppConfig(BaseModel):
  runtime: str = Field(
    default="python",
    description="Function App runtime: python, node, dotnet, java",
  )
  runtime_version: str = Field(
    default="3.13",
    description="Runtime version (e.g., 3.13 for Python, 20 for Node)",
  )
  sku: str = Field(
    default="FlexConsumption",
    description="Function App SKU: FlexConsumption, Consumption, Premium, Dedicated",
  )
  name_suffix: str = Field(
    default="01",
    description="Suffix for the Function App name, e.g. func-wd360-<project>-<env>-01",
  )
  ai_keys: Dict[str, str] = Field(
    default_factory=dict,
    description="AI provider API keys (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY)",
  )

  @field_validator("ai_keys", mode="before")
  @classmethod
  def coerce_ai_keys_to_strings(cls, v: Any) -> Dict[str, str]:
    """Ensure all AI key values are strings (YAML may parse numbers as int)."""
    if not isinstance(v, dict):
      return v
    return {k: str(val) for k, val in v.items()}


class AzureVmAiHostConfig(BaseModel):
  kind: str = Field(default="azure_vm_ai_host")
  project: str = Field(description="Short project identifier, e.g. mlproj")
  environment: str = Field(description="Environment name, e.g. dev, test, prod")
  location: str = Field(description="Azure region, e.g. westeurope")
  resource_group: str = Field(
    description="Azure resource group name (will be created if it doesn't exist)",
  )
  network_watcher_resource_group: str = Field(
    default="NetworkWatcherRG",
    description="Resource group where Network Watcher exists (default: NetworkWatcherRG)",
  )
  vm: VmConfig
  network: Optional[NetworkConfig] = Field(
    default=None,
    description="Network configuration (CIDRs auto-generated if not provided)",
  )
  tags: Dict[str, str] = Field(default_factory=dict)
  # Computed fields (shown in config but not required)
  vm_name: Optional[str] = Field(
    default=None,
    description="Computed VM name (auto-generated from project, environment, suffix)",
  )

  @field_validator("environment")
  @classmethod
  def validate_env(cls, value: str) -> str:
    v = value.lower()
    if v not in {"dev", "test", "stage", "prod"}:
      raise ValueError("environment must be one of: dev, test, stage, prod")
    return v

  @field_validator("project")
  @classmethod
  def validate_project(cls, value: str) -> str:
    if not value:
      raise ValueError("project must not be empty")
    if len(value) > 30:
      raise ValueError("project must be at most 30 characters")
    return value.lower()

  @field_validator("vm")
  @classmethod
  def validate_vm_auth(cls, vm: VmConfig) -> VmConfig:
    # Password is always required (will be auto-generated if not provided)
    # SSH key is optional for Linux
    if not vm.password and not vm.ssh_public_key:
      raise ValueError("Either password or ssh_public_key must be provided")
    return vm


class AzureFunctionAppAiHostConfig(BaseModel):
  kind: str = Field(default="azure_function_app_ai_host")
  project: str = Field(description="Short project identifier, e.g. mlproj")
  environment: str = Field(description="Environment name, e.g. dev, test, prod")
  location: str = Field(description="Azure region, e.g. eastus2")
  resource_group: str = Field(
    description="Azure resource group name (will be created if it doesn't exist)",
  )
  function_app: FunctionAppConfig
  existing_server_farm_id: Optional[str] = Field(
    default=None,
    description="Optional: Resource ID of existing App Service Plan to use (if not provided, one will be created)",
  )
  tags: Dict[str, str] = Field(default_factory=dict)
  # Computed fields
  function_app_name: Optional[str] = Field(
    default=None,
    description="Computed Function App name (auto-generated from project, environment, suffix)",
  )

  @field_validator("environment")
  @classmethod
  def validate_env(cls, value: str) -> str:
    v = value.lower()
    if v not in {"dev", "test", "stage", "prod"}:
      raise ValueError("environment must be one of: dev, test, stage, prod")
    return v

  @field_validator("project")
  @classmethod
  def validate_project(cls, value: str) -> str:
    if not value:
      raise ValueError("project must not be empty")
    if len(value) > 30:
      raise ValueError("project must be at most 30 characters")
    return value.lower()

  @field_validator("function_app")
  @classmethod
  def validate_runtime(cls, fa: FunctionAppConfig) -> FunctionAppConfig:
    if fa.runtime.lower() not in {"python", "node", "dotnet", "java"}:
      raise ValueError("runtime must be one of: python, node, dotnet, java")
    return fa


def load_config(path: Path) -> AzureVmAiHostConfig:
  """Load and validate an AzureVmAiHostConfig from a YAML or JSON file."""
  if not path.exists():
    raise FileNotFoundError(f"Config file not found: {path}")

  text = path.read_text(encoding="utf-8")
  data = yaml.safe_load(text)
  return AzureVmAiHostConfig.model_validate(data)


def load_function_app_config(path: Path) -> AzureFunctionAppAiHostConfig:
  """Load and validate an AzureFunctionAppAiHostConfig from a YAML or JSON file."""
  if not path.exists():
    raise FileNotFoundError(f"Config file not found: {path}")

  text = path.read_text(encoding="utf-8")
  data = yaml.safe_load(text)
  return AzureFunctionAppAiHostConfig.model_validate(data)


def generate_secure_password(length: int = 16) -> str:
  """Generate a secure random password meeting Azure VM requirements."""
  import secrets
  import string

  # Azure password requirements:
  # - At least 12 characters
  # - Contains uppercase, lowercase, numbers, and special characters
  alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
  password = "".join(secrets.choice(alphabet) for _ in range(length))
  # Ensure at least one of each required type
  if not any(c.isupper() for c in password):
    password = password[0].upper() + password[1:]
  if not any(c.islower() for c in password):
    password = password[0].lower() + password[1:]
  if not any(c.isdigit() for c in password):
    password = password[0] + "1" + password[1:]
  if not any(c in "!@#$%^&*" for c in password):
    password = password[0] + "!" + password[1:]
  return password


def auto_generate_network_cidrs(project: str, env: str) -> tuple[str, str]:
  """Auto-generate VNet and subnet CIDRs based on project/environment hash."""
  import hashlib

  # Deterministic but unique CIDRs per project/env
  h = hashlib.sha256(f"{project}-{env}".encode()).hexdigest()
  # Use different octets based on hash to avoid conflicts
  vnet_octet = int(h[:2], 16) % 240 + 10  # 10-250 range
  subnet_octet = int(h[2:4], 16) % 240 + 10
  return f"10.{vnet_octet}.0.0/16", f"10.{vnet_octet}.{subnet_octet}.0/24"


def dump_sample_config(path: Path) -> None:
  """Write a scaffolded sample config to the given path."""
  import secrets

  project = "myproject"
  environment = "dev"
  # Generate a secure password
  generated_password = generate_secure_password()
  # Auto-generate network CIDRs
  vnet_cidr, subnet_cidr = auto_generate_network_cidrs(project, environment)
  # Compute VM name
  vm_name_computed = f"vm-wd360-{project}-{environment}-01".lower()

  sample = {
    "kind": "azure_vm_ai_host",
    "project": project,
    "environment": environment,
    "location": "westeurope",
    "resource_group": f"rg-wd360-{project}-{environment}",  # Standardized RG name
    "network_watcher_resource_group": "NetworkWatcherRG",  # Where Network Watcher exists
    "vm_name": vm_name_computed,  # Show computed VM name
    "vm": {
      "os": "linux",
      "size": "Standard_D4s_v5",
      "admin_username": "devops",
      "password": generated_password,  # Auto-generated strong password
      "name_suffix": "01",
      # ssh_public_key is optional - comment it out
      # "ssh_public_key": "ssh-rsa AAAA...optional-for-linux",
    },
    # Network CIDRs are auto-generated, but shown for reference
    "network": {
      "vnet_cidr": vnet_cidr,  # Auto-generated
      "subnet_cidr": subnet_cidr,  # Auto-generated
    },
    "tags": {
      "owner": "team-ml",
      "cost_center": "CC123",
    },
  }
  serialized = yaml.safe_dump(sample, sort_keys=False, default_flow_style=False)
  path.write_text(serialized, encoding="utf-8")


def dump_sample_function_app_config(path: Path) -> None:
  """Write a scaffolded sample Function App config to the given path."""
  project = "myproject"
  environment = "dev"
  # Compute Function App name
  func_name_computed = f"func-wd360-{project}-{environment}-01".lower()

  sample = {
    "kind": "azure_function_app_ai_host",
    "project": project,
    "environment": environment,
    "location": "eastus2",
    "resource_group": f"rg-wd360-{project}-{environment}",
    "function_app_name": func_name_computed,  # Show computed Function App name
    "function_app": {
      "runtime": "python",
      "runtime_version": "3.13",
      "sku": "FlexConsumption",
      "name_suffix": "01",
      "ai_keys": {
        # AI provider API keys - set these for your deployment
        "OPENAI_API_KEY": "sk-...your-openai-key",
        "ANTHROPIC_API_KEY": "sk-ant-...your-anthropic-key",
        # Add other keys as needed: AZURE_OPENAI_API_KEY, etc.
      },
    },
    "tags": {
      "owner": "team-ml",
      "cost_center": "CC123",
    },
  }
  serialized = yaml.safe_dump(sample, sort_keys=False, default_flow_style=False)
  path.write_text(serialized, encoding="utf-8")


