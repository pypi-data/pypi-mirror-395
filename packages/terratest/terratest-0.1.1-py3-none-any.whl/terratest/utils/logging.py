import logging
from pathlib import Path
from typing import Optional

from terratest.utils.filesystem import ensure_base_dirs, get_job_log_file


def setup_root_logger(level: int = logging.INFO) -> None:
    """
    Logger base de la app (CLI/Web).
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def get_job_logger(job_id: str) -> logging.Logger:
    """
    Crea un logger específico para un job que escribe a:
    ~/.terratest/jobs/logs/{job_id}.log
    """
    ensure_base_dirs()
    logger_name = f"terratest.job.{job_id}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Evitar añadir múltiples handlers si se llama varias veces
    if not logger.handlers:
        log_file: Path = get_job_log_file(job_id)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
