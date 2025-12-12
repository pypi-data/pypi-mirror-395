## wd360 CLI

Python-based CLI framework for generating standardized Azure ARM templates for AI host infrastructure.

### Quick start

1. Create and activate a virtual environment (optional but recommended).
2. From the `cli/` directory, install the package in editable mode:

```bash
pip install -e .
```

3. Verify the CLI is available:

```bash
wd360 --help
```

### Current commands

- `wd360 init azure-vm`  
  Scaffold a starter configuration file for an Azure AI host VM stack.

- `wd360 plan azure-vm -c <config_file> -o <template_file>`  
  Load and validate config, then generate a basic ARM template skeleton for the stack.

Implementation is intentionally minimal at this stage and focuses on structure and naming conventions. Further resource details can be added incrementally.


