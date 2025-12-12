import os

from mtcli.conf import config

SYMBOL = os.getenv("SYMBOL", config["DEFAULT"].get("symbol", fallback="WIN$N"))
PERIOD = os.getenv("PERIOD", config["DEFAULT"].get("period", fallback="M1"))
LIMIT = int(os.getenv("LIMIT", str(config["DEFAULT"].getint("limit", fallback=566))))
RANGE = float(os.getenv("RANGE", str(config["DEFAULT"].get("range", fallback="100"))))
BY = os.getenv("BY", config["DEFAULT"].get("by", fallback="tpo"))
IB = int(os.getenv("IB", str(config["DEFAULT"].getint("ib", fallback=30))))
DIGITOS = int(
    os.getenv("DIGITOS", str(config["DEFAULT"].getint("digitos", fallback=0)))
)
