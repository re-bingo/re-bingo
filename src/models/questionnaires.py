from tortoise import Model, fields

from .users import UserItem


class QuestionnaireItem(Model):
    id: int = fields.IntField(pk=True)
    creator: UserItem = fields.ForeignKeyField("models.UserItem")
    title: str = fields.CharField(max_length=63)
    description: str = fields.TextField()

    class Meta:
        table = "questionnaires"
