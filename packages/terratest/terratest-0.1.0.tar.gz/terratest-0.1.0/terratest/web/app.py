from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from terratest.web.routes.jobs import router as jobs_router
from terratest.web.routes.job_files import router as job_files_router
from terratest.web.routes.job_file_read import router as job_file_read_router
from terratest.web.routes.filesystem import router as filesystem_router
from terratest.web.routes.docker_image import router as docker_image_router

app = FastAPI(title="Terratest WebUI")

STATIC_DIR = Path(__file__).parent / "static"

# Servir carpeta estática
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root():
    index = STATIC_DIR / "index.html"
    return FileResponse(index)

app.include_router(jobs_router, prefix="/api/jobs")
app.include_router(job_files_router)
app.include_router(job_file_read_router)
app.include_router(filesystem_router)
app.include_router(docker_image_router, prefix="/api/docker-image")

@app.get("/health")
def health():
    return {"status": "ok"}

