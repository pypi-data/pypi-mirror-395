import click
import sys
import os
import subprocess
import tomllib 
import rich_click as click
from pathlib import Path

@click.command(help="Open a shell with the project's virtual environment activated.")
def venv():
    project_dir = Path.cwd()
    config_path = project_dir / "psycor.toml"

    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    venv_path = project_dir / data.get("venv", {}).get("path", ".venv")

    if not venv_path.exists():
        raise click.ClickException("The virtual environment does not exist." "Please run 'psycor install' first.'")
    
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(venv_path)

    if sys.platform.startswith("win"):
        bin_dir = venv_path / "Scripts"
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
        shell = os.environ.get("COMSPEC", "cmd.exe")
        cmd = [shell]
    else:
        bin_dir = venv_path / "bin"
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
        shell = os.environ.get("SHELL", "/bin/bash")
        cmd = [shell]

    click.echo("Opening an active virtual environment shell...")
    click.echo("Type 'exit' when you are done to return.")

    subprocess.run(cmd, env=env)