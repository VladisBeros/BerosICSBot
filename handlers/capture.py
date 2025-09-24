from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from BerosICSBot.services.data_from_ics import zaglushka

router = Router()

@router.message(Command("capture"))
async def handle_start(message: Message):
    ics_e810t = zaglushka()
    data = []

    for ics in ics_e810t:
        data.append(str(ics))

    await message.answer(
        "[СПИСОК ICS У ЯКИХ ПРОБЛЕМИ З ЕКВАЙЄРОМ]\n" + "\n".join(data)
    )