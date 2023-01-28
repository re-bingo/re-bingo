from contextlib import suppress

import strawberry
from tortoise.exceptions import IntegrityError

from src.common.patch import auto_get_item_fields
from src.models.questions import QuestionItem, QuestionType
from src.types.lazy import Questionnaire


@auto_get_item_fields
@strawberry.type
class Question:
    id: int
    title: str
    prompt: str | None
    type: strawberry.enum(QuestionType)

    @strawberry.field
    async def questionnaire(self) -> Questionnaire:
        return Questionnaire(self.item.questionnaire)


async def add_question(questionnaire_id: int, title: str, prompt: str, type: QuestionType) -> Question | None:
    with suppress(IntegrityError):
        item = await QuestionItem.create(questionnaire_id=questionnaire_id, title=title, prompt=prompt, type=type.value)
        return Question(item)
