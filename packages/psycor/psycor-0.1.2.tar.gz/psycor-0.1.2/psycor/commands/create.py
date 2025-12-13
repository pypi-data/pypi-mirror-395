import click
import shutil
import tomllib
import tomli_w
import rich_click as click
from rich.console import Console, Group
from rich.panel import Panel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
path = BASE_DIR / "templates"

TEMPLATES = []

console = Console()

for directory in path.iterdir():
    TEMPLATES.append(directory.name)

@click.command(help="Create a new project")
@click.argument("name", required=False)
@click.option("--template", "-t", required=True, help="Template name to use.")
@click.option("--list", "list_templates", is_flag=True, help="List available templates..")
def create(name, template, list_templates):
    if list_templates:
        template = [f"[magenta]•[/magenta] {template}" for template in TEMPLATES]
        template_list = Group(*template)
        console.print(Panel(template_list, title="[green]Templates[/green]"))
        return
    
    if not name:
        raise click.UsageError("You must provide a project name: create NAME [--template ...]")
    
    new_path = Path(name)

    if new_path.exists():
        raise click.UsageError(f"A directory named '{name}' already exists. Choose another name or remove the existing one.")
    
    new_path.mkdir()

    last_path = path/template

    for archive in last_path.glob('*'):
        if archive.is_file():
            shutil.copy2(archive, new_path)
        elif archive.is_dir():
            shutil.copytree(archive, new_path / archive.name)

    path_toml = new_path / "psycor.toml"

    data = tomllib.loads(path_toml.read_text(encoding="utf-8"))
    data.setdefault("project", {})["name"] = name
    new_content = tomli_w.dumps(data)

    path_toml.write_text(new_content, encoding="utf-8")

    console.print("\n[green]✔  Project created.[/green]\n")