from telebot import TeleBot
from BerosICSBot.services.data_from_ics import packet_handler

def register_capture_handler(bot: TeleBot):
    @bot.message_handler(commands=['capture'])
    def handle_capture(message):
        ics_e810t = packet_handler()
        data = []

        for ics in ics_e810t:
            data.append(str(ics))

        bot.send_message(
            message.chat.id,
            "[СПИСОК ICS У ЯКИХ ПРОБЛЕМИ З ЕКВАЙЄРОМ]\n" + "\n".join(data)
        )