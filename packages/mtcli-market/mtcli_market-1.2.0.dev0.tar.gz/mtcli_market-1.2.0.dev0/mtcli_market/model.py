from collections import OrderedDict, defaultdict
import datetime
from math import ceil, floor
from typing import Any

import MetaTrader5 as mt5

from mtcli.logger import setup_logger
from mtcli.mt5_context import mt5_conexao

log = setup_logger()


def _mapear_timeframe(timeframe: str | int) -> int:
    mapping = {
        "M1": mt5.TIMEFRAME_M1,
        "M2": mt5.TIMEFRAME_M2,
        "M3": mt5.TIMEFRAME_M3,
        "M4": mt5.TIMEFRAME_M4,
        "M5": mt5.TIMEFRAME_M5,
        "M6": mt5.TIMEFRAME_M6,
        "M10": mt5.TIMEFRAME_M10,
        "M12": mt5.TIMEFRAME_M12,
        "M15": mt5.TIMEFRAME_M15,
        "M20": mt5.TIMEFRAME_M20,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H2": mt5.TIMEFRAME_H2,
        "H3": mt5.TIMEFRAME_H3,
        "H4": mt5.TIMEFRAME_H4,
        "H6": mt5.TIMEFRAME_H6,
        "H8": mt5.TIMEFRAME_H8,
        "H12": mt5.TIMEFRAME_H12,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1,
    }
    if isinstance(timeframe, int):
        minutos = timeframe
    else:
        tf_str = str(timeframe).upper().strip()
        if tf_str in mapping:
            return mapping[tf_str]
        minutos = 1
        if tf_str.endswith("M"):
            minutos = int(tf_str[:-1] or 1)
        elif tf_str.endswith("H"):
            minutos = int(tf_str[:-1] or 1) * 60
        elif tf_str.endswith("D"):
            minutos = int(tf_str[:-1] or 1) * 1440

    if minutos <= 1:
        return mt5.TIMEFRAME_M1
    elif minutos <= 5:
        return mt5.TIMEFRAME_M5
    elif minutos <= 15:
        return mt5.TIMEFRAME_M15
    elif minutos <= 30:
        return mt5.TIMEFRAME_M30
    elif minutos <= 60:
        return mt5.TIMEFRAME_H1
    elif minutos <= 240:
        return mt5.TIMEFRAME_H4
    else:
        return mt5.TIMEFRAME_D1


#####################################################################
# NOVA FUNÇÃO – obter_rates
#####################################################################
def obter_rates(symbol: str, timeframe: str | int, limit: int):
    tf = _mapear_timeframe(timeframe)

    with mt5_conexao():
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, limit)

    if rates is None or len(rates) == 0:
        log.warning(f"Nenhum rate retornado para {symbol} no timeframe {timeframe}")
        return []

    return rates


#####################################################################
# NOVA FUNÇÃO – estatísticas do dia (sempre D1)
#####################################################################
def obter_estatisticas_do_dia(symbol: str):
    rates = obter_rates(symbol, "D1", 1)

    if not rates:
        return None

    r = rates[0]

    return {
        "abertura": float(r["open"]),
        "fechamento": float(r["close"]),
        "maxima": float(r["high"]),
        "minima": float(r["low"]),
    }


def _range_blocks(low: float, high: float, block: float) -> list[float]:
    """Lista de blocos de preço cobrindo [low, high], ordem decrescente."""
    if block <= 0:
        return []
    low_b = floor(low / block) * block
    high_b = ceil(high / block) * block
    blocks = []
    b = high_b
    while b >= low_b:
        blocks.append(round(b, 8))
        b -= block
    return blocks


def _distribuir_volume_uniforme(
    volume: float, blocks: list[float]
) -> dict[float, float]:
    if not blocks:
        return {}
    per = volume / len(blocks)
    return {b: per for b in blocks}


def _distribuir_volume_por_overlap(
    low: float, high: float, block: float
) -> dict[float, float]:
    """Distribui volume proporcional ao overlap entre barra e bloco."""
    blocks = _range_blocks(low, high, block)
    if not blocks:
        return {}
    dist = {}
    for b in blocks:
        block_low = b - block
        block_high = b
        overlap_low = max(low, block_low)
        overlap_high = min(high, block_high)
        overlap = max(0.0, overlap_high - overlap_low)
        dist[b] = overlap

    total = sum(dist.values())
    if total <= 0:
        return _distribuir_volume_uniforme(1.0, blocks)
    return {b: dist[b] / total for b in dist}


def calcular_profile(
    rates,
    block: float,
    by: str = "tpo",
    ib_minutes: int = 30,
    va_percent: float = 0.7,
    timeframe: str | int = "M1",
) -> dict[str, Any]:
    # ✅ Proteção correta
    if rates is None or len(rates) == 0:
        return {
            "profile": {},
            "tpo": {},
            "total_volume": 0,
            "total_tpo": 0,
            "poc": None,
            "vah": None,
            "val": None,
            "va_prices": [],
            "hvn": [],
            "lvn": [],
            "ib": None,
            "rates_count": 0,
            "by": by,
            "block": block,
            "va_percent": va_percent,
            "timeframe": timeframe,
        }

    profile = defaultdict(float)
    tpo = defaultdict(int)

    # --- Distribuição (TPO, tick volume, real volume) ---
    for r in rates:
        low = float(r["low"])
        high = float(r["high"])

        tick_vol = float(r["tick_volume"]) if "tick_volume" in r.dtype.names else 0.0
        real_vol = (
            float(r["real_volume"]) if "real_volume" in r.dtype.names else tick_vol
        )

        blocks = _range_blocks(low, high, block)

        if by == "tpo":
            for b in blocks:
                tpo[b] += 1
                profile[b] += 1

        elif by == "tick":
            weights = _distribuir_volume_por_overlap(low, high, block)
            for b, w in weights.items():
                profile[b] += w * tick_vol
                tpo[b] += 1

        elif by == "real":
            volume = real_vol or tick_vol
            weights = _distribuir_volume_por_overlap(low, high, block)
            for b, w in weights.items():
                profile[b] += w * volume
                tpo[b] += 1

    # Ordenações
    ordered_profile = OrderedDict(
        sorted(profile.items(), key=lambda x: x[0], reverse=True)
    )
    ordered_tpo = OrderedDict(sorted(tpo.items(), key=lambda x: x[0], reverse=True))

    total_volume = sum(ordered_profile.values())
    total_tpo = sum(ordered_tpo.values())

    poc = (
        max(ordered_profile.items(), key=lambda x: x[1])[0] if ordered_profile else None
    )

    # --- Value Area ---
    def calcular_value_area(profile_map: dict[float, float], percent: float):
        if not profile_map:
            return None, None, []
        target = sum(profile_map.values()) * percent
        itens = sorted(profile_map.items(), key=lambda x: x[1], reverse=True)
        acum = 0
        escolhidos = []
        for price, vol in itens:
            escolhidos.append(price)
            acum += vol
            if acum >= target:
                break
        return max(escolhidos), min(escolhidos), escolhidos

    vah, val, va_prices = calcular_value_area(dict(ordered_profile), va_percent)

    # --- HVN e LVN ---
    hvn, lvn = [], []
    if ordered_profile:
        vols = list(ordered_profile.values())
        media = sum(vols) / len(vols)
        desvio = (sum((v - media) ** 2 for v in vols) / len(vols)) ** 0.5

        for price, vol in ordered_profile.items():
            if vol >= media + desvio:
                hvn.append(price)
            elif vol <= max(0.0, media - desvio):
                lvn.append(price)

    # =====================================================================
    #  INITIAL BALANCE (IB)
    # =====================================================================

    last_ts = rates[-1]["time"]
    d0 = datetime.datetime.fromtimestamp(last_ts).date()

    inicio_dia = datetime.datetime(d0.year, d0.month, d0.day, 0, 0)
    inicio_dia_ts = int(inicio_dia.timestamp())

    limite_ts = inicio_dia_ts + ib_minutes * 60

    ib_rates = [r for r in rates if inicio_dia_ts <= r["time"] <= limite_ts]

    if ib_rates:
        ib_high = max(r["high"] for r in ib_rates)
        ib_low = min(r["low"] for r in ib_rates)
        ib = {"high": ib_high, "low": ib_low}
    else:
        ib = None

    # =====================================================================

    return {
        "profile": ordered_profile,
        "tpo": ordered_tpo,
        "total_volume": total_volume,
        "total_tpo": total_tpo,
        "poc": poc,
        "vah": vah,
        "val": val,
        "va_prices": va_prices,
        "hvn": hvn,
        "lvn": lvn,
        "ib": ib,
        "rates_count": len(rates),
        "by": by,
        "block": block,
        "va_percent": va_percent,
        "timeframe": timeframe,
    }
