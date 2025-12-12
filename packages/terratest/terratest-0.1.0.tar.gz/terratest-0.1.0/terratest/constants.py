from pathlib import Path

APP_NAME = "terratest"

CONFIG_DIR = Path.home() / ".terratest"
JOBS_DIR = CONFIG_DIR / "jobs"
WORKSPACE_DIR = JOBS_DIR / "workspace"
OUTPUTS_DIR = JOBS_DIR / "outputs"
LOGS_DIR = JOBS_DIR / "logs"

# Por si luego quieres cambiar la imagen de Docker
DEFAULT_TERRAFORM_IMAGE = "terratest/terraform:latest"