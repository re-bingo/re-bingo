from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.common import auth
from src.db import close, connect, retry_when_lose_sql_connection
from src.types import schema

app = FastAPI(title="Re:Bingo", version="0.1.0", description=open("./README.md", encoding="utf-8").read())
app.add_event_handler("startup", connect)
app.add_event_handler("shutdown", close)
app.include_router(GraphQLRouter(schema, context_getter=auth.get_context), prefix="/graphql", tags=["GraphQL"])
app.include_router(auth.router)
app.add_middleware(CORSMiddleware, allow_origins="*", allow_credentials=True, allow_methods="*", allow_headers="*")
app.middleware("http")(retry_when_lose_sql_connection)
