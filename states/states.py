from aiogram.fsm.state import StatesGroup, State

class RegisterProfile(StatesGroup):
    random = State()
    gpt = State()
    dialog = State()
    qwiz = State()
    translate = State()
    set_system = State()
    resume = State()