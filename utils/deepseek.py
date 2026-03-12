from aiogram.fsm.context import FSMContext
from openai import AsyncOpenAI



class AI:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def set_system_prompt(self, prompt: str, state: FSMContext):
        messages = [{'role': 'system', 'content': prompt}]
        await state.update_data(messages=messages)

    async def get_answer(self, message:str, state: FSMContext):
        messages = (await state.get_data())['messages'] + [{'role': 'user', 'content': message}]
        while len(messages) > 20:
            messages.pop(1)
        response = await self.client.chat.completions.create(messages=messages, model=self.model)
        await state.update_data(messages=messages + [response.choices[0].message])
        return response.choices[0].message.content






