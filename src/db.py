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


SQL_CONFIG = dict(
    connections=load_sql_config(), use_tz=True, timezone="UTC",
    apps={"models": {"models": ["src.models.user", "aerich.models"], "default_connection": "default"}}
)


async def connect():
    await Tortoise.init(SQL_CONFIG)
    logger.success("tortoise initialized")
    if __debug__:
        from tortoise.exceptions import OperationalError
        try:
            await Tortoise.generate_schemas(safe=False)
            return logger.info("tortoise generated schemas")
        except OperationalError as err:
            logger.warning(repr(err.args[0]))
        from aerich import Command
        command = Command(tortoise_config=SQL_CONFIG)
        await command.init()
        await command.migrate()
        await command.upgrade()
        logger.info("aerich migrated schemas")


async def close():
    await Tortoise.close_connections()
    logger.success("tortoise connections closed")
