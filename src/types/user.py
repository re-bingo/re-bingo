from contextlib import suppress
from datetime import date, datetime
from hashlib import md5
from time import time

import orjson
import strawberry
from graphql import OperationType
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from strawberry.types import Info
from tortoise import exceptions

from src.common import salt
from src.common.patch import auto_get_item_fields
from src.models.users import UserItem


class Token(BaseModel):
    id: int
    time: float


@strawberry.type
class EduBackground:
    school: str | None = strawberry.field(lambda self: self.get("school"))


@strawberry.input
class EduBackgroundIn:
    school: str | None


@auto_get_item_fields
@strawberry.type
class User:
    id: int
    username: str | None
    email: str | None
    avatar: str | None
    birthday: str | None
    edu_background: EduBackground | None
    registered_at: datetime
    last_modified: datetime
    last_login_at: datetime

    @strawberry.field
    def token(self, info: Info) -> str | None:
        if info.operation.operation is OperationType.MUTATION:
            return generate_token(self)


def generate_token(user: UserItem | User):
    payload = orjson.dumps(Token(id=user.id, time=time()).dict())
    return f"{payload.decode()} {md5(payload + salt).hexdigest()}"


def parse_token(token: str) -> Token | None:
    with suppress(ValueError, AttributeError):
        payload, signature = token.split(" ")
        payload = payload.encode()
        if md5(payload + salt).hexdigest() == signature:
            return Token(**orjson.loads(payload))


async def get_user(user_id: int) -> User | None:
    with suppress(exceptions.DoesNotExist):
        item = await UserItem.get(id=user_id)
        return User(item)


async def add_user(username: str, password: str, email: str, avatar: str | None = None) -> User | None:
    with suppress(exceptions.IntegrityError):
        item = await UserItem.create(
            username=username, password=pbkdf2_sha256.hash(password), email=email, avatar=avatar
        )
        return User(item)


async def update_user(info: Info, username: str | None = None, email: str | None = None, avatar: str | None = None,
                      birthday: date | None = None, edu_background: EduBackgroundIn | None = None) -> User:
    item = await UserItem.get(id=info.context["token"].id)
    if username:
        item.username = username
    if email:
        item.email = email
    if avatar:
        item.avatar = avatar
    if birthday:
        item.birthday = birthday
    if edu_background:
        item.edu_background.update(edu_background.__dict__)
    await item.save()
    return User(item)
