from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.voice)
async def handle_voice(message: Message):
    await message.answer("I received your voice message!")

