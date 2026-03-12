# from handlers import *
from aiogram import Router
from handlers import (user_handlers, voice_handler, command_handlers, translate_handlers, resume_handlers,
                      gpt_handlers)
router = Router()
router.include_routers(user_handlers.router, voice_handler.router, command_handlers.router,
                       translate_handlers.router, resume_handlers.router, gpt_handlers.router)