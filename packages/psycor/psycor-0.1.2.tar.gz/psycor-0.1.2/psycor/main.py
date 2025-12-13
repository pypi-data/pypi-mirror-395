import click
import rich_click as click
from psycor.commands.create import create
from psycor.commands.install import install
from psycor.commands.venv import venv
from psycor.commands.add import add
from psycor.commands.init import init

@click.group()
def psycor():
    pass

psycor.add_command(create)
psycor.add_command(install)
psycor.add_command(venv)
psycor.add_command(add)
psycor.add_command(init)

if __name__ == '__main__':
    psycor()