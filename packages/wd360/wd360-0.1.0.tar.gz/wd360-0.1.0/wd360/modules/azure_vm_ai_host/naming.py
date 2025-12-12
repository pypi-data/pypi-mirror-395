from __future__ import annotations

import hashlib

from wd360.config.models import AzureVmAiHostConfig


def _hash_suffix(source: str, length: int = 6) -> str:
  """Deterministic short hash for names that must be globally unique."""
  h = hashlib.sha1(source.encode("utf-8")).hexdigest()
  return h[:length]


def vm_name(cfg: AzureVmAiHostConfig) -> str:
  return f"vm-wd360-{cfg.project}-{cfg.environment}-{cfg.vm.name_suffix}".lower()


def vnet_name(cfg: AzureVmAiHostConfig) -> str:
  return f"vnet-wd360-{cfg.project}-{cfg.environment}".lower()


def subnet_name(cfg: AzureVmAiHostConfig) -> str:
  return f"snet-ai-host-{cfg.environment}".lower()


def nsg_name(cfg: AzureVmAiHostConfig) -> str:
  return f"nsg-wd360-{cfg.project}-{cfg.environment}".lower()


def storage_account_name(cfg: AzureVmAiHostConfig) -> str:
  """
  Azure storage accounts: 3-24 chars, lowercase letters and numbers only.

  We want a recognizable wd360 suffix, but storage accounts cannot contain
  underscores. So we standardize on the suffix "wd360ai" and ensure it is
  always preserved at the end of the name.
  """
  suffix = "wd360ai"
  max_len = 24
  prefix_len = max_len - len(suffix)
  base = f"st{cfg.project}{cfg.environment}{_hash_suffix(cfg.project + cfg.environment)}"
  # Keep only allowed characters (letters/numbers) and lowercase
  base = "".join(ch for ch in base.lower() if ch.isalnum())
  prefix = base[:prefix_len]
  name = f"{prefix}{suffix}"
  # Final safety: trim to max length
  return name[:max_len]


def flow_logs_container_name() -> str:
  # Container names can include hyphens; keep suffix explicit
  return "flowlogs_wd360_ai_container"


def log_analytics_workspace_name(cfg: AzureVmAiHostConfig) -> str:
  return f"law-wd360-{cfg.project}-{cfg.environment}".lower()


