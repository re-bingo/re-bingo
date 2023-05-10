from enum import IntEnum

from tortoise import Model, fields


class QuestionType(IntEnum):
    completion = 1


class QuestionItem(Model):
    id: int = fields.IntField(pk=True)
    questionnaire = fields.ForeignKeyField("models.QuestionnaireItem")
    title: str = fields.CharField(max_length=31)
    prompt: str = fields.TextField()
    type: int = fields.IntEnumField(QuestionType)

    class Meta:
        table = "questions"
