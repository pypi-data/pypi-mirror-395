from fastapi import APIRouter
from pathlib import Path
from terratest.constants import OUTPUTS_DIR

router = APIRouter()

@router.get("/")
def list_jobs():
    jobs = []

    for job_dir in OUTPUTS_DIR.iterdir():
        if job_dir.is_dir():
            files = [f.name for f in job_dir.iterdir() if f.is_file()]
            jobs.append({
                "job_id": job_dir.name,
                "files": files
            })

    return jobs