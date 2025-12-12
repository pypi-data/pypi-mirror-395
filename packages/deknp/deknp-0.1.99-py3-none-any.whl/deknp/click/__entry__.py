from dektools.typer import command_version
from . import app
from . import env as env_command

command_version(app, __name__)
app.add_typer(env_command.app, name='env')


def main():
    app()
