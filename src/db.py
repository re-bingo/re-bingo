from tortoise import Tortoise
from loguru import logger


def load_sql_config():
    from pathlib import Path

    config_path = Path("./config/") / "sql.yaml"
    if config_path.is_file():
        from yaml import load, CLoader
        with open("./config/sql.yaml") as f:
            db_url = load(f, CLoader)
            logger.info(f"{db_url = }")
            return db_url
    else:
        logger.error("no db config provided")
        raise NotImplementedError


async def connect():
    await Tortoise.init(dict(
        connections=load_sql_config(), apps={"models": {"models": [__name__]}}, use_tz=True, timezone="UTC"
    ))
    logger.success("tortoise initialized")
    if __debug__:
        await Tortoise.generate_schemas(safe=True)
        logger.info("tortoise generated schemas")


async def close():
    await Tortoise.close_connections()
    logger.success("tortoise connections closed")
