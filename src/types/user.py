from contextlib import suppress
from hashlib import md5
from time import time

import orjson
import strawberry
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from tortoise import exceptions

from src.common import datetime, salt
from src.common.patch import auto_get_item_fields
from src.models.users import UserItem


class Token(BaseModel):
    id: int
    time: float


@auto_get_item_fields
@strawberry.type
class User:
    id: int
    username: str | None
    avatar: str | None
    registered_at: datetime
    last_modified: datetime
    last_login_at: datetime


def generate_token(user: UserItem | User):
    payload = orjson.dumps(Token(id=user.id, time=time()).dict())
    return f"{payload.decode()} {md5(payload + salt).hexdigest()}"


def parse_token(token: str) -> Token | None:
    if token:
        payload, signature = token.split(" ")
        payload = payload.encode()
        if md5(payload + salt).hexdigest() == signature:
            return Token(**orjson.loads(payload))


async def get_user(user_id: int) -> User | None:
    with suppress(exceptions.DoesNotExist):
        item = await UserItem.get(id=user_id)
        return User(item)


async def add_user(username: str, password: str, avatar: str | None = None) -> User | None:
    with suppress(exceptions.IntegrityError):
        item = await UserItem.create(username=username, password=pbkdf2_sha256.hash(password), avatar=avatar)
        return User(item)
