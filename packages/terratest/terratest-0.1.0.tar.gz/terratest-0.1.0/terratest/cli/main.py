import typer
from terratest.cli.commands.run import run_command
from terratest.cli.commands.web import web_command

app = typer.Typer(help="CLI de Terratest")

app.command("run")(run_command)
app.command("web")(web_command)