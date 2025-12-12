from pathlib import Path
import shutil
import os

from terratest.constants import CONFIG_DIR, JOBS_DIR, WORKSPACE_DIR, OUTPUTS_DIR, LOGS_DIR


def ensure_base_dirs() -> None:
    """
    Crea la estructura base:
    ~/.terratest/
        jobs/workspace/
        jobs/outputs/
        jobs/logs/
    """
    for path in [CONFIG_DIR, JOBS_DIR, WORKSPACE_DIR, OUTPUTS_DIR, LOGS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def copy_tree(src: Path, dst: Path) -> None:
    """
    Copia el contenido de src a dst (como cp -r).
    Si dst existe, se mezcla (no se borra).
    """
    src = src.resolve()
    dst = dst.resolve()

    if not src.exists() or not src.is_dir():
        raise FileNotFoundError(f"Directorio de origen no válido: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def safe_remove(path: Path) -> None:
    """
    Borra archivos o directorios de forma segura.
    """
    if not path.exists():
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def get_job_workspace_dir(job_id: str) -> Path:
    return WORKSPACE_DIR / job_id


def get_job_output_dir(job_id: str) -> Path:
    return OUTPUTS_DIR / job_id


def get_job_log_file(job_id: str) -> Path:
    return LOGS_DIR / f"{job_id}.log"
