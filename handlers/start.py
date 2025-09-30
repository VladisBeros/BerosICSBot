from telebot import TeleBot

def register_start_handler(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(
            message.chat.id,
            "Вас вітає BerosICSBot - телеграм бот для перевірки ICS-E810T на став відправку пакетів до еквайєру!"
        )