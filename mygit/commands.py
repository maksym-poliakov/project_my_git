import click
from .menu_navigator_class import MenuNavigator
from .menu import menu_structure as ms ,menu_default as m_default
from .unknownexception import UnknownException
from .files_class import Files

@click.command()
def init():
    """Инициализировать новый проект."""
    click.echo("Проект инициализирован!")

@click.command()
def status():
    """Показать статус проекта."""
    click.echo("Статус: работа в процессе.")

user = MenuNavigator(1)
@click.command()
def menu() :
    try:
        if not Files.search_file(Files.pwd(),Files.NAME_FILE_CONFIG) :
            user.navigator(m_default)

        user.navigator(ms)
    except UnknownException  as e:
        print(e)