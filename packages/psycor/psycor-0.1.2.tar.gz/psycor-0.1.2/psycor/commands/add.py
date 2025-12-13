import click
import subprocess
import sys
import tomllib
import tomli_w
import rich_click as click
from pathlib import Path

@click.command(help="Add and install packages into the project virtual environment.")
@click.argument("packages", nargs=-1)
def add(packages):
    project_dir = Path.cwd()
    config_path = project_dir / "psycor.toml"

    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    deps = data.get("dependencies", {})
    runtime = deps.get("runtime", [])

    venv_path = project_dir / data.get("venv", {}).get("path", ".venv")

    if not venv_path.exists():
        raise click.ClickException( "The virtual environment does not exist. " "Please run 'psycor install' first.")
    
    if sys.platform.startswith("win"):
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        pip_exe = venv_path / "bin" / "pip"

    click.echo(f"Installing {packages} into the virtual environment...")
    subprocess.run([str(pip_exe), "install", *packages], check=True)


    for pkg in packages:
        if pkg not in runtime:
            runtime.append(pkg)

    data.setdefault("dependencies", {})["runtime"] = runtime

    new_content = tomli_w.dumps(data)
    config_path.write_text(new_content, encoding="utf-8")

    click.echo(f"Dependency '{packages}' installed and added them to the TOML file.")