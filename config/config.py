from dataclasses import dataclass
from environs import Env
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@dataclass
class TgBot:
    token: str
    webhook_url: str
    admin_id: int


@dataclass
class AI:
    api_key: str
    base_url: str
    model: str


@dataclass
class Config:
    tg_bot: TgBot
    ai: AI


def load_config(path: str | None = None) -> Config:
    # if 'CONTEINER' not in os.environ:
    #     path = '.env_local'
    #     logging.info('Запуск вне контейнера')
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), webhook_url=env('WEBHOOK_URL'), admin_id=env.int('ADMIN_ID')),
                  ai=AI(api_key=env('AI_TOKEN'), base_url=env('AI_BASE_URL'), model=env('AI_MODEL')))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(load_config().tg_bot.token)
    print(load_config().tg_bot.webhook_url)
