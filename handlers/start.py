from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "Вас вітає BerosICSBot - телеграм бот для перевірки ICS-E810T на став відправку пакетів до еквайєру!"
    )