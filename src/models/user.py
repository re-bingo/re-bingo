import strawberry
from tortoise import Model, fields, exceptions


@strawberry.type
class User:
    id: int
    username: str | None
    avatar: str | None


class UserItem(Model):
    id: int = fields.IntField(pk=True)
    username: str | None = fields.CharField(15, null=True, unique=True, index=True)
    password: str | None = fields.CharField(31)
    avatar: str | None = fields.TextField(null=True)

    class Meta:
        name = "User"
        table = "users"
        data_fields = ["id", "username", "avatar"]


@strawberry.field
async def get_user(user_id: int) -> User | None:
    try:
        item = await UserItem.get(id=user_id)
    except exceptions.DoesNotExist:
        return None
    return User(id=item.id, username=item.username, avatar=item.avatar)


@strawberry.mutation
async def add_user(username: str, password: str, avatar: str = None) -> User | None:
    try:
        item = await UserItem.create(username=username, password=password, avatar=avatar)
    except exceptions.IntegrityError as err:
        return
    return User(id=item.id, username=item.username, avatar=item.avatar)
