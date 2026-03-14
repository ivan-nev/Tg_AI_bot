from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_command import LEXICON


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description) for command, description in LEXICON['main_menu'].items()
    ]
    await bot.set_my_commands(main_menu_commands)


def create_menu_inline() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON['inline_menu'].items()]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


def create_menu_translate() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key, style='danger') for key, value in
               LEXICON['keyboard_translate'].items()]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


def create_menu_resume() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value[0], callback_data=key, style=value[1]) for key, value in
               LEXICON['keyboard_resume'].items()]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()

def create_menu_stop() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⛔️ Закончить', callback_data='stop')],
        ]
    )

def create_menu_random() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON['keyboard_random'].items()]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()

def create_menu_chat() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON['keyboard_talk'].items()]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()

def create_menu_talk() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON['keyboard_talk_menu'].items()]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()

def create_menu_quiz() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON['keyboard_quiz'].items()]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()

def create_menu_quiz_menu() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON['keyboard_quiz_menu'].items()]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()