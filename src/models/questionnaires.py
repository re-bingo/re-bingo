from datetime import datetime
from enum import Enum

from tortoise import Model, fields

from .users import UserItem


class QuestionnaireType(str, Enum):
    online = "online"
    offline = "offline"


class QuestionnaireItem(Model):
    id: int = fields.IntField(pk=True)
    creator: UserItem = fields.ForeignKeyField("models.UserItem")
    title: str = fields.CharField(max_length=63)
    description: str = fields.TextField()
    start_date: datetime = fields.DatetimeField(null=True)
    end_date: datetime = fields.DatetimeField(null=True)
    school: str = fields.CharField(max_length=63, null=True)
    type: str = fields.CharEnumField(QuestionnaireType, null=True)
    location: str = fields.CharField(max_length=255, null=True)
    reward: str = fields.CharField(max_length=255, null=True)
    group_chat_qr_code_url: str = fields.CharField(max_length=255, null=True)
    poster_url: str = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "questionnaires"
