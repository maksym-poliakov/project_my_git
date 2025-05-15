import click

@click.group()
def cli():
    """Командная строка для управления вашим проектом."""
    pass

from .commands import init, status,menu

cli.add_command(init)
cli.add_command(status)
cli.add_command(menu)

if __name__ == '__main__':
    cli()