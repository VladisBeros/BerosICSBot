from aiogram import Bot, types

async def set_menu_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Привітання"),
        types.BotCommand(command="capture", description="Отримання даних по ICS")
    ])