import typer
import uvicorn

def web_command(port: int = 8765):
    typer.echo(f"🌐 Iniciando Terratest Web UI en http://localhost:{port}")
    uvicorn.run("terratest.web.app:app", host="0.0.0.0", port=port, reload=True)
