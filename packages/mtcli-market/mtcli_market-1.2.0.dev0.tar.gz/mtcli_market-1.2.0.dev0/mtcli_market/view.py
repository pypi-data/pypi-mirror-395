from typing import Any

import click

from .conf import DIGITOS


def _format_num(v, digitos):
    if v is None:
        return "–"
    if isinstance(v, int):
        return str(v)
    try:
        if digitos <= 0:
            if float(v).is_integer():
                return str(int(round(float(v))))
            return str(round(float(v)))
        fmt = f"{{:.{digitos}f}}"
        return fmt.format(float(v))
    except Exception:
        return str(v)


def exibir_profile(
    resultado: dict[str, Any], symbol: str, verbose: bool = False
) -> None:
    if not resultado:
        click.echo(f"Nenhum dado para exibir para o ativo {symbol}.")
        return

    profile = resultado.get("profile", {})
    tpo = resultado.get("tpo", {})

    poc = resultado.get("poc")
    vah = resultado.get("vah")
    val = resultado.get("val")
    hvn = resultado.get("hvn", [])
    lvn = resultado.get("lvn", [])
    ib = resultado.get("ib")
    estat = resultado.get("estatisticas_dia", {})
    total_vol = resultado.get("total_volume")
    total_tpo = resultado.get("total_tpo", sum(tpo.values()) if tpo else None)

    click.echo("")
    click.echo("-" * 60)
    click.echo(
        f"Market Profile para {symbol} — by {resultado.get('by')} — bloco {resultado.get('block')}"
    )
    click.echo("-" * 60)
    click.echo("")

    if verbose:
        if estat:
            click.echo("INFORMAÇÕES DO DIA (TF D1):")
            click.echo(f"Abertura:   {_format_num(estat['abertura'], DIGITOS)}")
            click.echo(f"Fechamento: {_format_num(estat['fechamento'], DIGITOS)}")
            click.echo(f"Máxima:     {_format_num(estat['maxima'], DIGITOS)}")
            click.echo(f"Mínima:     {_format_num(estat['minima'], DIGITOS)}")
            click.echo("")

        click.echo(
            "DISTRIBUIÇÃO DE PERFIL (preço : valor) — do preço mais alto para o mais baixo:"
        )
        prices = list(profile.keys())
        if prices:
            max_price_len = max(len(_format_num(p, DIGITOS)) for p in prices)
            click.echo(f"{'PREÇO'.ljust(max_price_len)}   VALOR")
            click.echo(f"{'-' * max_price_len}   -----")
        for price, vol in profile.items():
            click.echo(
                f"{_format_num(price, DIGITOS).ljust(max_price_len)} : {_format_num(vol, DIGITOS)}"
            )

        if total_vol is not None:
            click.echo(f"Total acumulado: {_format_num(total_vol, DIGITOS)}.")
        if total_tpo is not None and resultado.get("by") == "time":
            click.echo(f"Total de TPOs: {total_tpo}.")

        if poc is not None:
            click.echo(f"POC: {_format_num(poc, DIGITOS)}.")
        if val is not None and vah is not None:
            click.echo(
                f"Value Area: {_format_num(val, DIGITOS)} (baixo) — {_format_num(vah, DIGITOS)} (alto)."
            )

        if hvn:
            click.echo(f"HVNs: {', '.join(_format_num(p, DIGITOS) for p in hvn)}.")
        if lvn:
            click.echo(f"LVNs: {', '.join(_format_num(p, DIGITOS) for p in lvn)}.")

        if ib:
            click.echo(
                f"IB: {_format_num(ib['low'], DIGITOS)} — {_format_num(ib['high'], DIGITOS)}."
            )

        if tpo:
            click.echo("")
            click.echo("TPOs por faixa:")
            for price, cnt in tpo.items():
                click.echo(f"{_format_num(price, DIGITOS)} : {cnt}")

    else:
        click.echo("DISTRIBUICAO:")
        for price, vol in profile.items():
            click.echo(f"{_format_num(price, DIGITOS)} {_format_num(vol, DIGITOS)}")
        if poc:
            click.echo(f"POC {_format_num(poc, DIGITOS)}")
        if val and vah:
            click.echo(f"VA {_format_num(val, DIGITOS)}:{_format_num(vah, DIGITOS)}")
        if hvn:
            click.echo(f"HVNs {', '.join(_format_num(p, DIGITOS) for p in hvn)}")
        if lvn:
            click.echo(f"LVNs {', '.join(_format_num(p, DIGITOS) for p in lvn)}")
        if ib:
            click.echo(
                f"IB {_format_num(ib['low'], DIGITOS)}:{_format_num(ib['high'], DIGITOS)}"
            )
    click.echo("")
