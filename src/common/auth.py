from fastapi import Depends, Request, APIRouter, Body
from starlette.responses import Response, PlainTextResponse
from starlette.background import BackgroundTask
from src.models.user import Token, parse_token
from tortoise import exceptions
from src.models import UserItem, generate_token
from passlib.hash import pbkdf2_sha256
from src.common import timestamp
from pydantic import BaseModel
from contextlib import suppress


def find_token(r: Request) -> Token:
    return parse_token(r.headers.get("Authorization") or r.cookies.get("token") or r.query_params.get("token"))


def get_context(token: Token = Depends(find_token)):
    return {"token": token}


router = APIRouter(tags=["Auth"])


class LoginInput(BaseModel):
    username: str
    password: str


async def get_token(data: LoginInput) -> str | None:
    with suppress(exceptions.DoesNotExist):
        item = await UserItem.get(username=data.username)
        if pbkdf2_sha256.verify(data.password, item.password):
            return generate_token(item)


@router.post("/login", responses={404: {}})
async def login(data: LoginInput):
    if token := await get_token(data):
        response = PlainTextResponse(token, background=BackgroundTask(
            lambda: UserItem.filter(id=Token(token).id).update(last_login_at=timestamp())
        ))
        response.set_cookie("token", token)
    else:
        response = Response(status_code=404)
    return response
