from pathlib import Path
from typing import Tuple, List


class ValidationError(Exception):
    pass


def validate_module_path(module_path: str | Path) -> Path:
    """
    Normaliza y valida el path del módulo.
    - Debe existir
    - Debe ser directorio
    - Debe contener al menos un archivo .tf
    """
    path = Path(module_path).expanduser().resolve()

    if not path.exists():
        raise ValidationError(f"El módulo no existe: {path}")

    if not path.is_dir():
        raise ValidationError(f"El módulo no es un directorio: {path}")

    tf_files = list(path.glob("*.tf"))
    if not tf_files:
        raise ValidationError(f"El módulo no contiene archivos .tf: {path}")

    return path


def validate_terraform_files(path: Path) -> List[Path]:
    """
    Devuelve la lista de archivos .tf válidos en el módulo.
    Lanza error si no hay ninguno.
    """
    tf_files = sorted(path.glob("*.tf"))
    if not tf_files:
        raise ValidationError(f"No se encontraron archivos .tf en {path}")
    return tf_files
