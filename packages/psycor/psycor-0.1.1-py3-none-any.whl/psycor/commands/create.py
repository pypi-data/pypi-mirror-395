import click
import shutil
import tomllib
import tomli_w
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
path = BASE_DIR / "templates"

TEMPLATES = []

for c in path.iterdir():
    TEMPLATES.append(c.name)

@click.command(help="Create a new project")
@click.argument("name", required=False)
@click.option("--template", "-t", required=False, help="Template name to use.")
@click.option("--list", "list_templates", is_flag=True, help="List available templates..")
def create(name, template, list_templates):
    if list_templates:
        click.echo("Templates:")
        for t in TEMPLATES:
            click.echo(f" - {t}")
        return
    
    if not name:
        raise click.UsageError("You must provide a project name: create NAME [--template ...]")
    
    if template is None:
        raise click.ClickException("You must select a template with --template." "Use --list to view options.")

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

    click.echo("Project created.")