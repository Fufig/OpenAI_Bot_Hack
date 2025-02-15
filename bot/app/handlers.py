from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

import bot.app.database.requests as rq
from bot.app.gpt.gpt_handler import get_chatgpt_response

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет от Latoken')


@router.message(F.text)
async def handle_text_message(message: Message):
    chatgpt_response = await get_chatgpt_response(message.text)

    await rq.add_message(tg_id=message.from_user.id, message=message.text, response=chatgpt_response)

    await message.answer(chatgpt_response)