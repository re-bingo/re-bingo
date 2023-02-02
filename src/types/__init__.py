from src.types.lazy import *
from src.types.question import *
from src.types.questionnaire import *
from src.types.user import *


@strawberry.type
class Query:
    get_user = strawberry.field(get_user)
    get_questionnaire = strawberry.field(get_questionnaire)

    @strawberry.field
    async def greet(self, info: Info) -> str:
        token = info.context["token"]
        if token:
            return f"Hello, User({token.id})!"
        else:
            return "Hello, who are you?"


@strawberry.type
class Mutation:
    add_user = strawberry.mutation(add_user)
    add_questionnaire = strawberry.mutation(add_questionnaire)
    add_question = strawberry.mutation(add_question)


schema = strawberry.Schema(Query, Mutation)
