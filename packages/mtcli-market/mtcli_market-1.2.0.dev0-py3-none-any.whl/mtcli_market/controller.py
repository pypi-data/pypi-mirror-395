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
):
    # Normalização / validação de parâmetros
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

    rates = obter_rates(symbol, period, limit)

    resultado = calcular_profile(
        rates=rates,
        block=block,
        by=by,
        ib_minutes=ib_minutes,
        va_percent=va_percent,
        timeframe=period,
    )

    if not resultado:
        resultado = {}

    estatisticas = obter_estatisticas_do_dia(symbol)
    resultado["estatisticas_dia"] = estatisticas

    return resultado
