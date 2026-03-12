from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from states.states import RegisterProfile
from utils import AI
from keyboards import create_menu_inline, create_menu_translate, create_menu_stop

router = Router()


@router.callback_query(F.data == "chatgpt")
async def chatgpt_handler(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await state.set_state(RegisterProfile.gpt)
    await callback.answer()
    text = await callback.message.edit_text(text="минуточку...", action=ChatAction.TYPING)
    try:
        photo = FSInputFile("resources/images/gpt.png")
        await callback.message.answer_photo(photo=photo, caption=(
            '<b>Режим ChatGPT</b>\n\n'
            'Напиши любой вопрос - я отвечу'
            'Контекст диалога сохраняется'
            'Нажми <b>Закончить</b> чтобы выйти'
        ), reply_markup=create_menu_stop())
    except Exception as e:
        await callback.message.answer(text=('<b>Режим ChatGPT</b>\n\n'
                                            'Напиши любой вопрос - я отвечу'
                                            'Контекст диалога сохраняется'
                                            'Нажми <b>Закончить</b> чтобы выйти'), reply_markup=create_menu_stop())
    with open("resources/prompts/gpt.txt", "r") as f:
        system_message = f.read()
    await ai_client.set_system_prompt(system_message, state)
    await text.delete()

@router.message(F.text, RegisterProfile.gpt)
async def gpt_handler(message: Message, state: FSMContext, ai_client: AI):
    text = await message.answer(text="Ожидайте ответа...", action=ChatAction.TYPING)
    ai_answer = await ai_client.get_answer(message.text, state)
    await text.edit_text(text=ai_answer, reply_markup=create_menu_stop())

@router.callback_query(F.data == "stop")
async def stop_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.answer()
    await callback.message.answer(text="Окей, я закончил", reply_markup=create_menu_inline())
