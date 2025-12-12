from .cli import profile


def register(cli):
    cli.add_command(profile, name="mp")
