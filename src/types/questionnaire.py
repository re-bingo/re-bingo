from contextlib import suppress

import strawberry
from strawberry.types import Info
from tortoise import exceptions

from src.common.patch import auto_get_item_fields
from src.models import QuestionItem, QuestionnaireItem, QuestionnaireType
from src.types.question import Question
from src.types.user import Token, User


@auto_get_item_fields
@strawberry.type
class Questionnaire:
    id: int
    creator: User
    title: str
    description: str
    start_date: str | None
    end_date: str | None
    school: str | None
    type: strawberry.enum(QuestionnaireType) | None
    location: str | None
    reward: str | None
    group_chat_qr_code_url: str | None
    poster_url: str | None

    @strawberry.field
    async def questions(self) -> list[Question]:
        results = await QuestionItem.filter(questionnaire_id=self.id).all()
        return list(map(Question, results))


async def get_questionnaire(questionnaire_id: int) -> Questionnaire | None:
    with suppress(exceptions.DoesNotExist):
        item = await QuestionnaireItem.get(id=questionnaire_id)
        return Questionnaire(item)


async def add_questionnaire(
        title: str | None, description: str | None, start_date: str | None, end_date: str | None, school: str | None,
        type: QuestionnaireType | None, location: str | None, reward: str | None, group_chat_qr_code_url: str | None,
        poster_url: str | None, info: Info
) -> Questionnaire:
    token: Token = info.context["token"]
    item = await QuestionnaireItem.create(
        creator_id=token.id,
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        school=school,
        type=type,
        location=location,
        reward=reward,
        group_chat_qr_code_url=group_chat_qr_code_url,
        poster_url=poster_url,
    )
    return Questionnaire(item)
