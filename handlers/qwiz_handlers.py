from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from states.states import Profile
from utils import AI
from keyboards import create_menu_inline, create_menu_quiz, create_menu_quiz_menu
from random import randint

router = Router()


@router.callback_query(F.data == "quiz")
async def start_qwiz(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    text = await call.message.answer('Cтартуем...')
    await state.set_state(Profile.qwiz)
    photo = FSInputFile('resources/images/quiz.jpg')
    await state.update_data({'score': {'right_answers': 0, 'wrong_answers': 0}})
    await call.message.answer_photo(photo, caption='Выберите тему Квиза:', reply_markup=create_menu_quiz())
    await text.delete()


@router.callback_query(F.data.endswith('-quiz'), Profile.qwiz)
async def qwiz(call: CallbackQuery, state: FSMContext, ai_client: AI):
    await call.answer()
    text = await call.message.answer('Ожидайте ответа...')
    with open('resources/prompts/quiz.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    await ai_client.set_system_prompt(system_prompt + call.data + '\n' + str(randint(0, 1000)), state)
    ai_answer = await ai_client.get_answer('задай вопрос', state)
    await text.edit_text(ai_answer)


@router.message(F.text, Profile.qwiz)
async def qwiz(message: Message, state: FSMContext, ai_client: AI):
    score = (await state.get_data())['score']
    text = await message.answer('Проверяю...', reply_markup=ReplyKeyboardRemove())
    answer = await ai_client.get_answer(message.text, state)
    try:
        ai_answer, next_question = answer.split('@@@')
        if "✅ Верно" in ai_answer:
            score['right_answers'] += 1
        if "❌ Неверно" in ai_answer:
            score['wrong_answers'] += 1
        await text.delete()
        await message.answer(f'{ai_answer} \n'
                             f'счёт ✅ {score["right_answers"]} : ❌ {score["wrong_answers"]} \n'
                             f'{next_question}', reply_markup=create_menu_quiz_menu())
    except Exception:
        await text.delete()
        await message.answer(answer, reply_markup=create_menu_quiz_menu())

@router.callback_query(F.data == "stop_quiz", Profile.qwiz)
async def stop_qwiz(call: CallbackQuery, state: FSMContext):
    score = (await state.get_data())['score']
    result = get_rusult(score)
    await call.answer()
    await call.message.edit_text(f'{result}', reply_markup=create_menu_inline())
    await state.clear()

@router.callback_query(F.data == "change_quiz", Profile.qwiz)
async def change_quiz(call: CallbackQuery, state: FSMContext):
    score = (await state.get_data())['score']
    result = get_rusult(score)
    await call.answer()
    await call.message.edit_text(f'{result}')
    await state.clear()
    await state.set_state(Profile.qwiz)
    await state.update_data({'score': {'right_answers': 0, 'wrong_answers': 0}})
    await call.message.answer('Выберите тему Квиза:', reply_markup=create_menu_quiz())


def get_rusult(score: dict)-> str:
    right = score['right_answers']
    wrong = score['wrong_answers']
    total = right + wrong
    if total < 3:
        return '🔬 Слишком мало вопросов'
    if right == total:
        return f'🤯 Ты просто гений! ✅{right} из {total}'
    if right / total > 0.7:
        return f'👍 Ты молодец! ✅{right} из {total}'
    if right / total > 0.3:
        return f'🙁 Надо потренироваться! ✅{right} из {total}'
    return f'🤮 Очень плохо! ❌{wrong} из {total}'
