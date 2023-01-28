from contextlib import suppress

from fastapi import APIRouter, Depends, Request
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.responses import PlainTextResponse, Response
from tortoise import exceptions

from src.common import timestamp
from src.models import UserItem
from src.types import Token, generate_token, parse_token


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
