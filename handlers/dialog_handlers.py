from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from states.states import Profile
from utils import AI
from keyboards import create_menu_inline, create_menu_chat, create_menu_talk

router = Router()


@router.callback_query((F.data == 'dialog') | (F.data == 'change'))
async def personality_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Выберите персонажа:', reply_markup=create_menu_chat())
    await state.set_state(Profile.dialog)


@router.callback_query(F.data.endswith('-personality'), Profile.dialog)
async def dialog_handler(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await callback.answer()
    text = await callback.message.answer('Диалог начат, секундочку...!', reply_markup=ReplyKeyboardRemove(),
                                         chat_action=ChatAction.TYPING)
    with open("resources/prompts/dialog.txt", "r", encoding='utf-8') as file:
        system_prompt = file.read() + callback.data.split("-")[0]
    await ai_client.set_system_prompt(system_prompt, state)
    ai_answer = await ai_client.get_answer('Привет!', state)
    await text.delete()
    await callback.message.answer(ai_answer, reply_markup=create_menu_talk())


@router.message(F.text , Profile.dialog)
async def dialog_handler_continue(message: Message, state: FSMContext, ai_client: AI):
    text = await message.answer('Диалог продолжается, секундочку...!')
    ai_answer = await ai_client.get_answer(message.text, state)
    await text.delete()
    await message.answer(ai_answer, reply_markup=create_menu_talk())

@router.callback_query(F.data == 'stop', Profile.dialog)
async def cancel_handler(callback:CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Вы отменили диалог', reply_markup=create_menu_inline())
