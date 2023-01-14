from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.models import schema
from src.db import connect, close

app = FastAPI(title="Re:Bingo", version="0.1.0", description=open("./README.md", encoding="utf-8").read())
app.add_event_handler("startup", connect)
app.add_event_handler("shutdown", close)
app.include_router(GraphQLRouter(schema), prefix="/graphql", tags=["GraphQL"])