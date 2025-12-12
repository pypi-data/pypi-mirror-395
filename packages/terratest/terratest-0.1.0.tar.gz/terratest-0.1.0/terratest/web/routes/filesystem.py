"""
Rutas para exploración del sistema de archivos
"""
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import List
import os

router = APIRouter(prefix="/api/filesystem", tags=["filesystem"])


@router.get("/project-dir")
async def get_project_directory():
    """
    Devuelve el directorio raíz del proyecto actual
    """
    try:
        # Obtener el directorio actual de trabajo
        project_dir = Path.cwd()
        return {
            "project_dir": str(project_dir),
            "normalized": str(project_dir).replace('\\', '/')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener directorio del proyecto: {str(e)}")


@router.get("/list")
async def list_directory(path: str = Query(".", description="Path del directorio a listar")):
    """
    Lista los directorios dentro de un path dado.
    Soporta paths relativos y absolutos.
    """
    try:
        # Convertir a Path y resolver
        if path == ".":
            dir_path = Path.cwd()
        else:
            dir_path = Path(path)
            # Si no es absoluto, hacerlo relativo al directorio actual
            if not dir_path.is_absolute():
                dir_path = Path.cwd() / dir_path
            dir_path = dir_path.resolve()
        
        # Verificar que existe y es un directorio
        if not dir_path.exists():
            raise HTTPException(status_code=404, detail=f"El directorio no existe: {path}")
        
        if not dir_path.is_dir():
            raise HTTPException(status_code=400, detail=f"La ruta no es un directorio: {path}")
        
        # Listar solo directorios (excluir archivos)
        directories = []
        try:
            for item in sorted(dir_path.iterdir()):
                # Solo incluir directorios, excluir algunos especiales
                if item.is_dir():
                    # Excluir directorios ocultos en Linux/Mac y algunos especiales
                    if item.name.startswith('.') and item.name not in ['.']:
                        continue
                    if item.name.startswith('__'):
                        continue
                    directories.append(item.name)
        except PermissionError:
            raise HTTPException(status_code=403, detail="Sin permisos para leer el directorio")
        
        # Información del path padre
        parent_path = None
        if dir_path.parent != dir_path:  # No estamos en la raíz
            parent_path = str(dir_path.parent)
        
        return {
            "path": str(dir_path),
            "normalized_path": str(dir_path).replace('\\', '/'),
            "parent": parent_path,
            "directories": directories,
            "count": len(directories)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar directorio: {str(e)}")
