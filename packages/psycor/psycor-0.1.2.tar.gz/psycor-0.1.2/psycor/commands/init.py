import click
import tomli_w
import rich_click as click
from rich.console import Console
from pathlib import Path

console = Console()

@click.command(help="Initialize Psycor configuration inside an existing project folder.")
def init():
    name_dir = Path.cwd().name

    config_data = {
        "project": {
            "name": name_dir,
            "python": "3.12"
        },
        "venv": {
            "path": ".venv"
        },
        "dependencies": {
            "runtime": [],
            "dev": [
                "pytest"
            ]
        },
        "commands": {
            "test": "pytest"
        }
    }

    toml_name = "psycor.toml"

    with open(toml_name, 'wb') as file:
        tomli_w.dump(config_data, file)
        
    console.print("\n✔ [green] Project initialized successfully![/green]\n")