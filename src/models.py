import strawberry


@strawberry.type
class Query:
    hello: str = strawberry.field(lambda: "hello from 🍓")


schema = strawberry.Schema(Query)
