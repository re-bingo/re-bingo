from datetime import datetime, timezone


def timestamp():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


salt = open("./config/salt", "rb").read()
