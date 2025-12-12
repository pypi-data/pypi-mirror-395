from __future__ import annotations

from wd360.config.models import AzureFunctionAppAiHostConfig


def function_app_name(cfg: AzureFunctionAppAiHostConfig) -> str:
  """Generate standardized Function App name."""
  return f"func-wd360-{cfg.project}-{cfg.environment}-{cfg.function_app.name_suffix}".lower()


def app_service_plan_name(cfg: AzureFunctionAppAiHostConfig) -> str:
  """Generate standardized App Service Plan name."""
  return f"asp-wd360-{cfg.project}-{cfg.environment}".lower()


def storage_account_name(cfg: AzureFunctionAppAiHostConfig) -> str:
  """Generate standardized storage account name for Function App (required for deployment)."""
  import hashlib
  import secrets
  
  # Azure storage accounts: 3-24 chars, lowercase letters and numbers only
  # Format: wd360ai_{project}_{env}_{hash} but without underscores (Azure doesn't allow them)
  # So it becomes: wd360ai{project}{env}{hash}
  # wd360ai prefix for standardization and AI workload identification
  
  # Use project name or generate random name if not provided
  project = cfg.project if cfg.project else f"proj{secrets.token_hex(3)}"
  
  base = f"{project}{cfg.environment}"
  suffix = hashlib.sha1(base.encode("utf-8")).hexdigest()[:6]
  name = f"wd360ai{base}{suffix}".lower()
  # Ensure max length 24
  return name[:24]


def app_insights_name(cfg: AzureFunctionAppAiHostConfig) -> str:
  """Generate standardized Application Insights name."""
  return f"appi-wd360-{cfg.project}-{cfg.environment}".lower()

