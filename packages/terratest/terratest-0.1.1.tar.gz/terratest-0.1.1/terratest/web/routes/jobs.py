from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional
import shutil
from terratest.core.executor import JobExecutor
from terratest.constants import OUTPUTS_DIR
from terratest.utils.config_store import get_config_store

router = APIRouter()

@router.post("/")
def run_job(
    module_path: str,
    enable_ssh: bool = Query(False, description="Habilitar autenticación SSH para Git"),
    ssh_key_path: Optional[str] = Query(None, description="Path personalizado a la clave SSH"),
    tf_cloud_token: Optional[str] = Query(None, description="Token de Terraform Cloud"),
    tf_cloud_org: Optional[str] = Query(None, description="Organización de Terraform Cloud"),
    tf_cloud_workspace: Optional[str] = Query(None, description="Workspace de Terraform Cloud"),
    aws_access_key_id: Optional[str] = Query(None, description="AWS Access Key ID"),
    aws_secret_access_key: Optional[str] = Query(None, description="AWS Secret Access Key"),
    aws_session_token: Optional[str] = Query(None, description="AWS Session Token (opcional)"),
):
    """
    Ejecutar un job de Terraform con configuración opcional:
    - SSH: Para repositorios privados de Git
    - Terraform Cloud: Para remote state y colaboración
    - AWS: Credenciales para proveedores de AWS
    """
    # Guardar configuración en store temporal
    config_store = get_config_store()
    config_data = {
        'enable_ssh': enable_ssh,
        'ssh_key_path': ssh_key_path,
        'tf_cloud_token': tf_cloud_token,
        'tf_cloud_org': tf_cloud_org,
        'tf_cloud_workspace': tf_cloud_workspace,
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'aws_session_token': aws_session_token,
    }
    config_store.update(config_data)
    
    executor = JobExecutor()
    return executor.execute_job(
        module_path=module_path,
        enable_ssh=enable_ssh,
        ssh_key_path=ssh_key_path,
        tf_cloud_token=tf_cloud_token,
        tf_cloud_org=tf_cloud_org,
        tf_cloud_workspace=tf_cloud_workspace,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
    )

@router.get("/")
def list_jobs():
    jobs = []
    
    if not OUTPUTS_DIR.exists():
        return jobs

    for job_dir in OUTPUTS_DIR.iterdir():
        if job_dir.is_dir():
            files = [f.name for f in job_dir.iterdir() if f.is_file()]
            jobs.append({
                "job_id": job_dir.name,
                "files": files,
                "modified_time": job_dir.stat().st_mtime
            })

    # Ordenar por fecha de modificación (más reciente primero)
    jobs.sort(key=lambda x: x["modified_time"], reverse=True)
    
    # Remover el campo modified_time antes de retornar
    for job in jobs:
        del job["modified_time"]

    return jobs

@router.delete("/all")
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