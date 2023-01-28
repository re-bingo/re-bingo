from datetime import datetime

from tortoise import Model, fields


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
