import typer
from rich import print

from terratest.core.executor import JobExecutor


def run_command(module_path: str):
    print("[bold cyan]🔧 Terratest — Ejecutando módulo[/bold cyan]")
    print(f"📁 Módulo: {module_path}")

    executor = JobExecutor()
    result = executor.execute_job(
        module_path=module_path,
        run_init=True,
        run_plan=True,
        run_apply=False,
    )

    job_id = result.get("job_id")
    status = result.get("status")

    if job_id:
        print(f"🆔 Job ID: [bold]{job_id}[/bold]")
    print(f"📊 Status: [bold]{status}[/bold]")

    # Info útil en FASE 1
    workspace = result.get("workspace_dir")
    output_dir = result.get("output_dir")
    if workspace:
        print(f"📂 Workspace: {workspace}")
    if output_dir:
        print(f"📂 Outputs:   {output_dir}")

    if "error" in result:
        print(f"[red]❌ Error:[/red] {result['error']}")
    else:
        print("[green]✔ Workspace preparado correctamente[/green]")