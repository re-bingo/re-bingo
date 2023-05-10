import strawberry
from strawberry.types import Info

from src.common.patch import auto_get_item_fields
from src.models.tags import TagItem
from src.types.lazy import User


@auto_get_item_fields
@strawberry.type
class Tag:
    name: str
    user: User


async def add_tag(name: str, info: Info) -> Tag:
    item = await TagItem.create(name=name, user_id=info.context["token"].id)
    return Tag(item)
