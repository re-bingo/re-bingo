from tortoise import Model, fields

from src.models.users import UserItem


class TagItem(Model):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(63)
    user: UserItem = fields.ManyToManyField("models.UserItem")

    class Meta:
        table = "tags"
