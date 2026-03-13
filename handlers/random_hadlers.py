from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from states.states import Profile
from utils import AI
from keyboards import create_menu_inline, create_menu_translate, create_menu_stop, create_menu_random

router = Router()


@router.callback_query(F.data == "random_fact")
async def random_fact(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await callback.answer()
    await state.set_state(Profile.random)
    answer = await callback.message.answer(text="Секунду...", reply_markup=ReplyKeyboardRemove(),
                                           action=ChatAction.TYPING)
    with open("resources/prompts/random_fackt.txt", "r") as f:
        prompt = f.read()
    await ai_client.set_system_prompt(prompt, state)
    ai_answer = await ai_client.get_answer('ещё факт', state)
    try:
        foto = FSInputFile("resources/images/random.png")
        await callback.message.answer_photo(foto, reply_markup=create_menu_random(), caption=ai_answer)
    except Exception as e:
        await answer.edit_text(text=ai_answer, reply_markup=create_menu_random())

@router.callback_query(F.data == "next", Profile.random)
async def next(callback: CallbackQuery, state: FSMContext, ai_client: AI):
    await callback.answer()
    await callback.message.edit_caption(caption="Секунду...")
    ai_answer = await ai_client.get_answer('ещё факт', state)
    await callback.message.edit_caption(caption=ai_answer, reply_markup=create_menu_random())

@router.callback_query(F.data == "stop", Profile.random)
async def stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Окей, я закончил", reply_markup=create_menu_inline())


