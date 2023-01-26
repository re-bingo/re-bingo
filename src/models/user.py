import strawberry
from tortoise import Model, fields, exceptions
from contextlib import suppress
from passlib.hash import pbkdf2_sha256
from hashlib import md5
from src.common import datetime, timestamp, salt
from time import time
from pydantic import BaseModel
import orjson


class Token(BaseModel):
    id: int
    time: float


class UserItem(Model):
    id: int = fields.IntField(pk=True)
    username: str | None = fields.CharField(15, null=True, unique=True, index=True)
    password: str | None = fields.CharField(87)
    avatar: str | None = fields.TextField(null=True)
    registered_at: datetime = fields.DatetimeField(auto_now_add=True)
    last_modified: datetime = fields.DatetimeField(auto_now=True)
    last_login_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
        data_fields = ["id", "username", "avatar"]

    def __str__(self):
        return f"<UserItem: {self.id} {self.username!r}>"


@strawberry.type
class User:
    id: int
    username: str | None
    avatar: str | None
    registered_at: datetime
    last_modified: datetime
    last_login_at: datetime

    def __init__(self, item: UserItem):
        self.item = item

    def __getattr__(self, field: str):
        return getattr(self.item, field)


def generate_token(user: UserItem | User):
    payload = orjson.dumps(Token(id=user.id, time=time()).dict())
    return f"{payload.decode()} {md5(payload + salt).hexdigest()}"


def parse_token(token: str):
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
