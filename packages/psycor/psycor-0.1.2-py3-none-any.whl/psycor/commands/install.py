import click
import subprocess
import sys
import venv
import tomllib
import rich_click as click
from pathlib import Path

@click.command(help="Create or update the virtual environment and install project dependencies.")
def install():
    project_dir = Path.cwd()
    config_path = project_dir / "psycor.toml"

    data = tomllib.loads(config_path.read_text(encoding="utf-8"))

    venv_path = project_dir / data.get("venv", {}).get("path", ".venv")

    deps_runtime = data.get("dependencies", {}).get("runtime", [])
    deps_dev = data.get("dependencies", {}).get("dev", [])

    if not deps_runtime and not deps_dev:
        click.echo("No dependencies defined in [dependencies].")
        return
    
    if not venv_path.exists():
        click.echo(f"Creating virtual environment at {venv_path}...")
        venv.EnvBuilder(with_pip=True).create(venv_path)
    else:
        click.echo(f"Virtual environment {venv_path} already exists. Using it.")

    if sys.platform.startswith("win"):
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        pip_exe = venv_path / "bin" / "pip"

    if not pip_exe.exists():
        raise click.ClickException(f"Could not find pip at {pip_exe}")
    
    packages = deps_runtime + deps_dev
    click.echo(f"Installing dependencies: {', '.join(packages)}")
    subprocess.run([str(pip_exe), "install", *packages], check=True)

    click.echo("Installation complete.")