import strawberry
from src.models.user import *


@strawberry.type
class Query:
    hello: str = strawberry.field(lambda: "hello from 🍓")
    user = get_user


@strawberry.type
class Mutation:
    user = add_user


schema = strawberry.Schema(Query, Mutation)
