from datetime import datetime, timezone
from pathlib import Path


def timestamp():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


config_root = Path("./config/")

salt = open(config_root / "salt", "rb").read()
