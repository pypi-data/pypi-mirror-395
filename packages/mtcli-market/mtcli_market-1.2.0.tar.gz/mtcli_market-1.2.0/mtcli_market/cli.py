"""
Interface de linha de comando (CLI) para exibição do Market Profile.
"""

import click

from .conf import (
    BY,
    IB,
    CRITERIO_HVN,
    LIMIT,
    PERIOD,
    RANGE,
    SYMBOL,
)
from .controller import obter_profile
from .view import exibir_profile


@click.command()
@click.version_option(package_name="mtcli-market")
@click.option(
    "--symbol", "-s", default=SYMBOL, show_default=True, help="Codigo do ativo."
)
@click.option(
    "--period",
    "-p",
    default=PERIOD,
    show_default=True,
    help="Timeframe do profile.",
)
@click.option(
    "--limit",
    "-l",
    default=LIMIT,
    show_default=True,
    type=int,
    help="Quantidade de timeframes do profile.",
)
@click.option(
    "--block",
    "-k",
    default=RANGE,
    show_default=True,
    type=float,
    help="Tamanho do bloco de pontos.",
)
@click.option(
    "--by",
    type=click.Choice(["tpo", "tick", "real"]),
    default=BY,
    show_default=True,
    help="Base para o profile.",
)
@click.option(
    "--initial-balance",
    "-ib",
    default=IB,
    show_default=True,
    type=int,
    help="Duracao em minutos do Initial Balance.",
)
@click.option(
    "--va-percent",
    "-va",
    default=0.7,
    show_default=True,
    type=float,
    help="Percentual da Value Area.",
)
@click.option(
    "--criterio-hvn",
    default=CRITERIO_HVN,
    type=click.Choice(["mult", "std", "percentil"]),
    show_default=True,
    help="Criterio para calculo de HVN/LVN.",
)
@click.option(
    "--mult-hvn",
    default=1.5,
    show_default=True,
    type=float,
    help="Multiplicador da media para HVN (criterio mult).",
)
@click.option(
    "--mult-lvn",
    default=0.5,
    show_default=True,
    type=float,
    help="Multiplicador da media para LVN (criterio mult).",
)
@click.option(
    "--percentil-hvn",
    default=90,
    show_default=True,
    type=float,
    help="Percentil superior para HVN.",
)
@click.option(
    "--percentil-lvn",
    default=10,
    show_default=True,
    type=float,
    help="Percentil inferior para LVN.",
)

@click.option(
    "--verbose",
    "-vv",
    is_flag=True,
    default=False,
    show_default=True,
    help="Modo verboso.",
)
def profile(
    symbol,
    period,
    limit,
    block,
    by,
    initial_balance,
    va_percent,
    criterio_hvn,
    mult_hvn,
    mult_lvn,
    percentil_hvn,
    percentil_lvn,
    verbose,
):
    """
    Calcula e exibe o Market Profile de um ativo.
    """

    if va_percent <= 0 or va_percent > 1:
        raise click.BadParameter("va-percent deve estar no intervalo (0, 1].")
    if block <= 0:
        raise click.BadParameter("Bloco deve ser maior que zero")

    resultado = obter_profile(
        symbol=symbol,
        period=period,
        limit=int(limit),
        block=float(block),
        by=by,
        ib_minutes=initial_balance,
        va_percent=va_percent,
        criterio_hvn=criterio_hvn,
        mult_hvn=mult_hvn,
        mult_lvn=mult_lvn,
        percentil_hvn=percentil_hvn,
        percentil_lvn=percentil_lvn,
    )

    exibir_profile(resultado, symbol=symbol, verbose=verbose)


if __name__ == "__main__":
    profile()
