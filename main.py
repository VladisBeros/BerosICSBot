import telebot
from config import load_config

def main():
    config = load_config()
    bot = telebot.TeleBot(config.BOT_TOKEN)

    from handlers import register_handlers
    register_handlers(bot)

    print("Bot is running...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()