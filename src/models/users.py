from datetime import date, datetime

from tortoise import Model, fields


class UserItem(Model):
    id: int = fields.IntField(pk=True)
    username: str = fields.CharField(15, null=True, unique=True, index=True)
    password: str | None = fields.CharField(87)
    email: str | None = fields.CharField(254, index=True)
    avatar: str | None = fields.TextField(null=True)
    birthday: date | None = fields.DateField(null=True, default=date.today)
    edu_background: dict | None = fields.JSONField(null=True)
    registered_at: datetime = fields.DatetimeField(auto_now_add=True)
    last_modified: datetime = fields.DatetimeField(auto_now=True)
    last_login_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
        data_fields = ["id", "username", "avatar"]

    def __str__(self):
        return f"<UserItem: {self.id} {self.username!r}>"
