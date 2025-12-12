from fastapi import APIRouter, HTTPException
from terratest.constants import OUTPUTS_DIR

router = APIRouter()

@router.get("/api/jobs/{job_id}/files/{filename}")
def read_job_file(job_id: str, filename: str):
    file_path = OUTPUTS_DIR / job_id / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Intentar leer con diferentes encodings
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    content = None
    
    for encoding in encodings_to_try:
        try:
            content = file_path.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        # Si ninguno funciona, leer como binario y decodificar con errors='replace'
        content = file_path.read_text(encoding='utf-8', errors='replace')
    
    return {"content": content}