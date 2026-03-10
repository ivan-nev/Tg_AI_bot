from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.states import RegisterProfile
from utils import AI
from keyboards import create_menu_inline, create_menu_translate

router = Router()
@router.callback_query(F.data == "translate")
async def translate(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await state.set_state(RegisterProfile.translate)
    with open("resources/prompts/translate.txt", "r", encoding='utf-8') as f:
        system_prompt = f.read()
    await ai_client.set_system_prompt(system_prompt, state)
    await callback.message.edit_text("Введите текст для перевода", reply_markup=create_menu_translate())

@router.message(F.text, RegisterProfile.translate)
async def translate_text(message: Message, state: FSMContext, ai_client: AI):
    translate = await message.answer("Translate...⚙️")
    answer = await ai_client.get_answer(message.text, state)
    await translate.edit_text(f'Translate --> \n{answer}', reply_markup=create_menu_translate())
    mes = (await state.get_data())['messages']
    while len(mes) > 1:
        mes.pop()

@router.callback_query(F.data == "stop", RegisterProfile.translate)
async def stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=callback.message.text)
    await callback.message.answer("Вы остановили перевод", reply_markup=create_menu_inline())