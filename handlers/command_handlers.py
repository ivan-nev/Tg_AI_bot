from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.states import RegisterProfile
from utils import AI
from keyboards import create_menu_inline

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    start_text = '''Привет! Я бот, твой помощник.
    Выбери тему из меню'''
    await message.answer(text=start_text, reply_markup=create_menu_inline())
    await state.clear()

@router.message(F.text == 'system')
async def set_system(message: Message, state: FSMContext):
    await message.answer(text='напиши системный промт')
    await state.set_state(RegisterProfile.set_system)

@router.message(F.text, RegisterProfile.set_system)
async def get_system(message: Message, state: FSMContext, ai_client: AI):
    await ai_client.set_system_prompt(message.text, state)
    await message.answer(text='системный промт установлен')
    await state.set_state(RegisterProfile.gpt)

# @router.message(F.text, RegisterProfile.gpt)
# async def get_text(message: Message, state: FSMContext, ai_client: AI):
#     answer = await ai_client.get_answer(message.text, state)
#     await message.answer(text=answer)


# @router.message(F.text, RegisterProfile.waiting_name)
# async def get_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer(f'Привет {message.text}\n'
#                          f'Шаг 2 из 3 - Сколько тебе лет?')
#     await state.set_state(RegisterProfile.waiting_age)
#
# @router.message(F.text, RegisterProfile.waiting_age)
# async def get_name(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await message.answer(f'Шаг 3 из 3 - Какой твой город?')
#     await state.set_state(RegisterProfile.waiting_city)
#
#
# @router.message(F.text, RegisterProfile.waiting_city)
# async def get_name(message: Message, state: FSMContext):
#     await state.update_data(city=message.text)
#     data = await state.get_data()
#     await message.answer(f'Спасибо, твои данные:\n {data}!\n')
#     await state.set_state(None)
