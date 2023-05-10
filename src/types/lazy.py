from typing import TYPE_CHECKING, Annotated

from strawberry import lazy

if TYPE_CHECKING:
    from src.types.question import Question
    from src.types.questionnaire import Questionnaire
    from src.types.tag import Tag
    from src.types.user import User
else:
    User = Annotated["User", lazy(".user")]
    Questionnaire = Annotated["Questionnaire", lazy(".questionnaire")]
    Question = Annotated["Question", lazy(".question")]
    Tag = Annotated["Tag", lazy(".tag")]

__all__ = ["User", "Questionnaire", "Question", "Tag"]
