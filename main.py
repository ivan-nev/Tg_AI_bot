import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import load_config
from handlers import router
from keyboards import set_main_menu
from utils import AI
from middlewares import AIClientMiddleware, ThrottlingMiddleware


# Загрузка конфигурации
config = load_config()

# Инициализация AI-клиента и бота
deepseek = AI(api_key=config.ai.api_key, base_url=config.ai.base_url, model=config.ai.model)
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))

# Диспетчер и middleware
dp = Dispatcher()
dp.include_router(router)
# dp.update.middleware(ThrottlingMiddleware())
dp.update.middleware(AIClientMiddleware(ai_client=deepseek))


async def on_startup(bot: Bot) -> None:
    await set_main_menu(bot)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


async def main() -> None:
    use_webhook = os.getenv("WEBHOOK", "False").lower() == "true"

    if use_webhook:
        # Настройки вебхука из переменных окружения
        WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
        WEBHOOK_PORT = int(os.getenv("PORT", 8080))

        if not WEBHOOK_URL:
            raise ValueError("Переменная окружения WEBHOOK_URL не установлена, но требуется для вебхука")

        # Создание aiohttp-приложения
        app = web.Application()

        # Регистрация обработчика вебхуков
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)

        # Подключение диспетчера и бота к приложению (для setup_application)
        setup_application(app, dp, bot=bot)

        # Установка вебхука в Telegram
        await bot.set_webhook(url=f"{WEBHOOK_URL}{WEBHOOK_PATH}")

        # Запуск сервера
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=WEBHOOK_PORT)
        await site.start()

        logging.info(f"Бот запущен в режиме webhook на порту {WEBHOOK_PORT}")

        # Ожидание завершения (блокируем основной корутиной)
        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()
            await bot.delete_webhook()
    else:
        # Режим polling
        await set_main_menu(bot)
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())