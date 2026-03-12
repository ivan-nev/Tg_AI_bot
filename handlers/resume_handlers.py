from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.states import RegisterProfile
from utils import AI
from keyboards import create_menu_inline, create_menu_resume

router = Router()

@router.callback_query(F.data == "resume")
async def resume_start(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await state.set_state(RegisterProfile.resume)
    await callback.answer()
    say = await callback.message.edit_text('Минуточку, обрабатываю...')
    with open("resources/prompts/resume.txt", "r", encoding='utf-8') as f:
        system_prompt = f.read()
    await ai_client.set_system_prompt(system_prompt, state)
    ai_answer = await ai_client.get_answer("", state)
    await say.edit_text(ai_answer, reply_markup=create_menu_resume())

@router.callback_query(F.data == 'next', RegisterProfile.resume)
async def resume_next(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await callback.answer()
    say = await callback.message.answer('Минуточку, обрабатываю...')
    ai_answer = await ai_client.get_answer("!next!", state)
    await callback.message.edit_text(text=callback.message.text)
    if '***' in ai_answer:
        await state.clear()
        await say.edit_text(ai_answer, reply_markup=create_menu_inline())
    else:
        await say.edit_text(ai_answer, reply_markup=create_menu_resume())

@router.callback_query(F.data == 'stop', RegisterProfile.resume)
async def resume_stop(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await callback.answer()
    say = await callback.message.answer('Минуточку, обрабатываю...')
    ai_answer = await ai_client.get_answer("!stop!", state)
    await state.clear()
    await say.edit_text(ai_answer, reply_markup=create_menu_inline())

@router.message(F.text, RegisterProfile.resume)
async def resume_text(message: Message, state: FSMContext, ai_client: AI):
    say = await message.answer('Минуточку, обрабатываю...')
    ai_answer = await ai_client.get_answer(message.text, state)
    if '***' in ai_answer:
        await state.clear()
        await say.edit_text(ai_answer, reply_markup=create_menu_inline())
    else:
        await say.edit_text(ai_answer, reply_markup=create_menu_resume())