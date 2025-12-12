from typing import Optional
import typer
from rich import print as rprint

from retgit import __version__
from retgit.commands.init import init_cmd
from retgit.commands.propose import propose_cmd
from retgit.commands.push import push_cmd
from retgit.commands.integration import integration_app
from retgit.commands.plugin import plugin_app
from retgit.plugins.version.commands import version_app, release_shortcut
from retgit.plugins.changelog.commands import changelog_app


def version_callback(value: bool):
    if value:
        rprint(f"[bold cyan]retgit[/bold cyan] version [green]{__version__}[/green]")
        raise typer.Exit()


app = typer.Typer(
    name="retgit",
    help="🧠 AI-powered Git workflow assistant with task management integration",
    no_args_is_help=True,
    rich_markup_mode="rich"
)


@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """RetGit - AI-powered Git workflow assistant"""
    pass


app.command("init")(init_cmd)
app.command("propose")(propose_cmd)
app.command("push")(push_cmd)
app.add_typer(integration_app, name="integration")
app.add_typer(plugin_app, name="plugin")

# Version and Changelog plugins
app.add_typer(version_app, name="version")
app.add_typer(changelog_app, name="changelog")

# Shortcut: rg release = rg version release
app.command("release")(release_shortcut)


def main():
    app()

if __name__ == "__main__":
    main()