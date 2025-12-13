"""
Camada de controle do módulo Market Profile.
"""

from mtcli.logger import setup_logger

from .model import (
    calcular_profile,
    obter_estatisticas_do_dia,
    obter_rates,
)

log = setup_logger()


def obter_profile(
    symbol: str,
    period: str,
    limit: int,
    block: float,
    by: str,
    ib_minutes: int = 30,
    va_percent: float = 0.7,
    criterio_hvn: str = "mult",
    mult_hvn: float = 1.5,
    mult_lvn: float = 0.5,
    percentil_hvn: float = 90,
    percentil_lvn: float = 10,
):
    """
    Orquestra a obtenção e cálculo do Market Profile.
    """

    if by not in ("tpo", "tick", "real"):
        log.warning(f"Parametro by invalido {by}. Usando tpo")
        by = "tpo"

    if va_percent <= 0 or va_percent > 1:
        log.warning("va_percent fora de intervalo (0,1]. Usando 0.7")
        va_percent = 0.7

    try:
        block = float(block)
    except Exception:
        log.warning(f"Bloco invalido {block}. Usando 1.0.")
        block = 1.0

    if criterio_hvn not in ("mult", "std", "percentil"):
        log.warning("criterio_hvn invalido. Usando mult.")
        criterio_hvn = "mult"

    rates = obter_rates(symbol, period, limit)

    resultado = calcular_profile(
        rates=rates,
        block=block,
        by=by,
        ib_minutes=ib_minutes,
        va_percent=va_percent,
        timeframe=period,
        criterio_hvn=criterio_hvn,
        mult_hvn=mult_hvn,
        mult_lvn=mult_lvn,
        percentil_hvn=percentil_hvn,
        percentil_lvn=percentil_lvn,
    )

    if not resultado:
        resultado = {}

    estatisticas = obter_estatisticas_do_dia(symbol)
    resultado["estatisticas_dia"] = estatisticas

    return resultado
