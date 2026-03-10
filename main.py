from aiogram import Bot, Dispatcher
import asyncio
from config import load_config
from handlers import router
from keyboards import set_main_menu
from utils import AI
from middlewares import AIClientMiddleware, ThrottlingMiddleware

config = load_config()
deepseek = AI(api_key=config.ai.api_key, base_url=config.ai.base_url, model=config.ai.model)
bot = Bot(token=config.tg_bot.token)

dp = Dispatcher()
dp.include_router(router)

dp.update.middleware(ThrottlingMiddleware())
dp.update.middleware(AIClientMiddleware(ai_client=deepseek))

async def main():
    await set_main_menu(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())