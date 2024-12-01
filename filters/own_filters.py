import asyncio

from aiogram.filters import Filter
from aiogram.types import Message

from database.core import Database
from base_config import env_values


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str] | str) -> None:
        if isinstance(chat_types, str):
            chat_types = [chat_types]
        self.chat_types = chat_types
    
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        admins = await Database.selectAdmin()
        return message.from_user.id in admins


class IsOwner(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in list(map(int, env_values["OWNERS"].split(";")))