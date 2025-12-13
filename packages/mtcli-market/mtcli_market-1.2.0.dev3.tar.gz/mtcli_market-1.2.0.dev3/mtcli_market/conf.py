"""
Módulo de configuração do mtcli-market.

Este módulo centraliza as configurações padrão utilizadas pelo plugin,
permitindo que os valores sejam sobrescritos via:

- Variáveis de ambiente (os.getenv)
- Arquivo de configuração global do mtcli

Parâmetros configuráveis:
- SYMBOL   : Ativo padrão
- PERIOD   : Timeframe padrão
- LIMIT    : Quantidade de candles
- RANGE    : Tamanho do bloco do Market Profile
- BY       : Base do profile (tpo, tick, real)
- IB       : Duração do Initial Balance em minutos
- DIGITOS  : Quantidade de casas decimais na exibição
"""

import os

from mtcli.conf import config


#: Código do ativo padrão
SYMBOL = os.getenv("SYMBOL", config["DEFAULT"].get("symbol", fallback="WIN$N"))

#: Timeframe padrão
PERIOD = os.getenv("PERIOD", config["DEFAULT"].get("period", fallback="M1"))

#: Quantidade de candles utilizados no profile
LIMIT = int(os.getenv("LIMIT", str(config["DEFAULT"].getint("limit", fallback=566))))

#: Tamanho do bloco de preço do Market Profile
RANGE = float(os.getenv("RANGE", str(config["DEFAULT"].get("range", fallback="100"))))

#: Tipo de base do profile: "tpo", "tick" ou "real"
BY = os.getenv("BY", config["DEFAULT"].get("by", fallback="tpo"))

#: Duração do Initial Balance em minutos
IB = int(os.getenv("IB", str(config["DEFAULT"].getint("ib", fallback=30))))

#: Quantidade de casas decimais para exibição no terminal
DIGITOS = int(
    os.getenv("DIGITOS", str(config["DEFAULT"].getint("digitos", fallback=0)))
)
