from typing import TYPE_CHECKING, Annotated

from strawberry import lazy

if TYPE_CHECKING:
    from src.types.question import Question
    from src.types.questionnaire import Questionnaire
    from src.types.user import User
else:
    User = Annotated["User", lazy(".user")]
    Questionnaire = Annotated["Questionnaire", lazy(".questionnaire")]
    Question = Annotated["Question", lazy(".question")]

__all__ = ["User", "Questionnaire", "Question"]
