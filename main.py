import asyncio
from aiogram import Bot, Dispatcher
from config import load_config
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_routers
from utils.set_menu_commands import set_menu_commands

async def main():
    config = load_config()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    register_routers(dp)
    await set_menu_commands(bot)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())