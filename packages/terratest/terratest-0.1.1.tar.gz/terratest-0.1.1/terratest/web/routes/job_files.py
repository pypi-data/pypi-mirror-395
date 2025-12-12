from fastapi import APIRouter, HTTPException
from terratest.constants import OUTPUTS_DIR

router = APIRouter()

@router.get("/api/jobs/{job_id}/files")
def list_job_files(job_id: str):
    folder = OUTPUTS_DIR / job_id
    if not folder.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "files": sorted([f.name for f in folder.iterdir() if f.is_file()])
    }