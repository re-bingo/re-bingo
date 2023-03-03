from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import OperationalError


def load_sql_config():
    from src.common import config_root

    config = config_root / "sql.yaml"
    if config.is_file():
        from yaml import CLoader, load
        with config.open() as f:
            db_url = load(f, CLoader)
            logger.info(f"{db_url = }")
            return db_url
    else:
        logger.error("no db config provided")
        raise NotImplementedError


SQL_CONFIG = dict(
    connections=load_sql_config(), use_tz=True, timezone="UTC",
    apps={"models": {"models": ["src.models", "aerich.models"], "default_connection": "default"}}
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
        from aerich import Command, exceptions
        command = Command(tortoise_config=SQL_CONFIG)
        try:
            await command.init()
            try:
                result = await command.upgrade()
            except OperationalError:
                logger.debug("no need to upgrade")
            else:
                logger.success(f"aerich upgraded {result}")
            finally:
                await command.migrate()
                logger.info("aerich migrated schemas")
        except (AttributeError, exceptions.NotSupportError) as err:
            from traceback import format_exception_only
            logger.error(format_exception_only(err)[0])


async def close():
    await Tortoise.close_connections()
    logger.success("tortoise connections closed")


async def retry_when_lose_sql_connection(request, call_next):
    try:
        return await call_next(request)
    except OperationalError as err:
        if "Lost connection to MySQL server during query" in str(err.args):
            logger.error(err)
            return await call_next(request)
        else:
            raise err
