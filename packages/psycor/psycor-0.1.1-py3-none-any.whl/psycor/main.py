import click
from psycor.commands.create import create
from psycor.commands.install import install
from psycor.commands.venv import venv
from psycor.commands.add import add

@click.group()
def psycor():
    pass

psycor.add_command(create)
psycor.add_command(install)
psycor.add_command(venv)
psycor.add_command(add)

if __name__ == '__main__':
    psycor()