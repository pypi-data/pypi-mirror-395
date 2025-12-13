"""
Módulo de registro do plugin mtcli-market.

Este módulo é responsável por registrar o comando `mp`
dentro da CLI principal do mtcli, permitindo que o usuário
execute o Market Profile via:

    mt mp

ou conforme alias configurado.
"""

from .cli import profile


def register(cli):
    """
    Registra o comando de Market Profile na CLI principal do mtcli.

    Args:
        cli: Objeto principal da aplicação mtcli responsável
             por gerenciar os comandos registrados.

    Returns:
        None
    """
    cli.add_command(profile, name="mp")
