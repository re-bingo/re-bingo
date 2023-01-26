# TODO: implement questions and choices, logic and paging, posting and attending

import strawberry
from strawberry.types import Info
from tortoise import Model, fields, exceptions
from contextlib import suppress
from src.models.user import UserItem, User, Token
from src.common.patch import auto_get_item_fields


class QuestionnaireItem(Model):
    id: int = fields.IntField(pk=True)
    creator: UserItem = fields.ForeignKeyField("models.UserItem")
    title: str = fields.CharField(max_length=63)
    description: str = fields.TextField()

    class Meta:
        table = "questionnaires"


@auto_get_item_fields
@strawberry.type
class Questionnaire:
    id: int
    creator: User
    title: str
    description: str


async def get_questionnaire(questionnaire_id: int) -> Questionnaire | None:
    with suppress(exceptions.DoesNotExist):
        item = await QuestionnaireItem.get(id=questionnaire_id)
        return Questionnaire(item)


async def add_questionnaire(title: str, description: str, info: Info) -> Questionnaire:
    token: Token = info.context["token"]
    item = await QuestionnaireItem.create(creator_id=token.id, title=title, description=description)
    return Questionnaire(item)
