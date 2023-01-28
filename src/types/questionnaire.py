# TODO: implement questions and choices, logic and paging, posting and attending

from contextlib import suppress

import strawberry
from strawberry.types import Info
from tortoise import exceptions

from src.common.patch import auto_get_item_fields
from src.models import QuestionItem, QuestionnaireItem
from src.types.question import Question
from src.types.user import Token, User


@auto_get_item_fields
@strawberry.type
class Questionnaire:
    id: int
    creator: User
    title: str
    description: str

    @strawberry.field
    async def questions(self) -> list[Question]:
        results = await QuestionItem.filter(questionnaire_id=self.id).all()
        return list(map(Question, results))


async def get_questionnaire(questionnaire_id: int) -> Questionnaire | None:
    with suppress(exceptions.DoesNotExist):
        item = await QuestionnaireItem.get(id=questionnaire_id)
        return Questionnaire(item)


async def add_questionnaire(title: str, description: str, info: Info) -> Questionnaire:
    token: Token = info.context["token"]
    item = await QuestionnaireItem.create(creator_id=token.id, title=title, description=description)
    return Questionnaire(item)
