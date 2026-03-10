from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from utils import AI


class AIClientMiddleware(BaseMiddleware):
    def __init__(self, ai_client: AI):
        self.client = ai_client


    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        data['ai_client'] = self.client
        result = await handler(event, data)

        return result
