import strawberry
from src.models.user import *
from src.models.questionnaire import *


@strawberry.type
class Query:
    get_user = strawberry.field(get_user)
    get_questionnaire = strawberry.field(get_questionnaire)

    @strawberry.field
    async def greet(self, info: Info) -> str:
        return f"Hello, User({info.context['token'].id})!"


@strawberry.type
class Mutation:
    add_user = strawberry.mutation(add_user)
    add_questionnaire = strawberry.mutation(add_questionnaire)


schema = strawberry.Schema(Query, Mutation)
