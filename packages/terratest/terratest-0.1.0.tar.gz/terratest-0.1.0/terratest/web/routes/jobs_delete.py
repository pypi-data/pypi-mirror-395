from fastapi import APIRouter, HTTPException
from pathlib import Path
import shutil
from terratest.constants import OUTPUTS_DIR

router = APIRouter()

@router.delete("/{job_id}")
def delete_job(job_id: str):
    """Eliminar un job específico"""
    job_dir = OUTPUTS_DIR / job_id
    
    if not job_dir.exists() or not job_dir.is_dir():
        raise HTTPException(status_code=404, detail="Job no encontrado")
    
    try:
        shutil.rmtree(job_dir)
        return {"message": f"Job {job_id} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar job: {str(e)}")

@router.delete("/")
def delete_all_jobs():
    """Eliminar todos los jobs"""
    if not OUTPUTS_DIR.exists():
        return {"message": "No hay jobs para eliminar"}
    
    deleted_count = 0
    errors = []
    
    for job_dir in OUTPUTS_DIR.iterdir():
        if job_dir.is_dir():
            try:
                shutil.rmtree(job_dir)
                deleted_count += 1
            except Exception as e:
                errors.append(f"{job_dir.name}: {str(e)}")
    
    if errors:
        return {
            "message": f"Se eliminaron {deleted_count} jobs con {len(errors)} errores",
            "deleted": deleted_count,
            "errors": errors
        }
    
    return {
        "message": f"Se eliminaron {deleted_count} jobs correctamente",
        "deleted": deleted_count
    }
