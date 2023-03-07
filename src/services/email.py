from random import randrange

from fastapi import APIRouter
from httpx import AsyncClient
from yaml import CLoader, load

from hashlib import md5

from ..common import config_root

with open(config_root / "env.yaml") as f:
    poster_url = load(f, CLoader)["poster"]

client = AsyncClient(base_url=poster_url)

router = APIRouter(tags=["Service"])


@router.post("/verify")
async def send_email(to: str):
    number = "".join(str(randrange(10)) for _ in range(5))
    payload = {"to": to, "title": number, "message": "", "nameFrom": "Bingo", "nameTo": ""}
    res = await client.post("/sendmail", json=payload)
    return {"captcha": md5(number.encode()).hexdigest(), "success": res.is_success}
