import strawberry
from tortoise import Model, fields, exceptions
from contextlib import suppress
from passlib.hash import pbkdf2_sha256


@strawberry.type
class User:
    id: int
    username: str | None
    avatar: str | None


class UserItem(Model):
    id: int = fields.IntField(pk=True)
    username: str | None = fields.CharField(15, null=True, unique=True, index=True)
    password: str | None = fields.CharField(87)
    avatar: str | None = fields.TextField(null=True)

    class Meta:
        name = "User"
        table = "users"
        data_fields = ["id", "username", "avatar"]

    def __str__(self):
        return f"<UserItem: {self.id} {self.username!r}>"


@strawberry.field
async def get_user(user_id: int) -> User | None:
    with suppress(exceptions.DoesNotExist):
        item = await UserItem.get(id=user_id)
        return User(id=item.id, username=item.username, avatar=item.avatar)


@strawberry.mutation
async def add_user(username: str, password: str, avatar: str = None) -> User | None:
    with suppress(exceptions.IntegrityError):
        item = await UserItem.create(username=username, password=pbkdf2_sha256.hash(password), avatar=avatar)
        return User(id=item.id, username=item.username, avatar=item.avatar)
