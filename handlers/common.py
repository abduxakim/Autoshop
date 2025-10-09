from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_IDS
from locales.help_texts import HELP_CLIENT, HELP_ADMIN

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer(HELP_ADMIN)
    else:
        await message.answer(HELP_CLIENT)
