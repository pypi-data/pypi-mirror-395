import typer
import uvicorn

from schug.cli import fetch, load
from schug.config import settings
from schug.load.demo import load_demo

cli = typer.Typer()


@cli.callback()
def callback():
    """
    Welcome to the CLI
    """


cli.add_typer(load.app, name="load", help="Load information into database")
cli.add_typer(fetch.app, name="fetch", help="Fetch data from sources")


@cli.command("serve")
def serve_app(reload: bool = typer.Option(False, "--reload")):
    """Start a dev server for the schug app"""
    typer.echo("Serving schug")
    app = "schug.main:app"
    uvicorn.run(app=app, host=settings.host, port=settings.port, reload=reload)


@cli.command("setup")
def setup_app(demo: bool = typer.Option(False, "--demo")):
    """Setup the service with some information"""
    typer.echo("Setting up schug")
    if demo:
        load_demo()
