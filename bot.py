import telebot
from telebot import types
import os

# Токен хранится в Render → Environment → TELEGRAM_TOKEN
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Қызмет түрлері")
    btn2 = types.KeyboardButton("📞 Байланыс / Жазылу")
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        "👋 Сәлеметсіз бе! *МедЦентр+* қабылдау бөлімі.\n"
        "Қажетті бөлімді таңдаңыз 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text == "📋 Қызмет түрлері":
        bot.send_message(
            message.chat.id,
            "🩺 Біздің негізгі қызметтер:\n"
            "• Терапевт — 8:00–20:00\n"
            "• Стоматолог — 9:00–19:00\n"
            "• Қан талдауы, УДЗ, ЭКГ\n\n"
            "Төмендегі батырма арқылы жазылуға болады 👇"
        )
    elif message.text == "📞 Байланыс / Жазылу":
        bot.send_message(
            message.chat.id,
            "📍 Шиелі Ғ.Мұратбаев 244\n"
            "📞 +7 (777) 123-45-67\n"
            "🕒 8:00–20:00"
        )
    else:
        bot.send_message(message.chat.id, "Төмендегі мәзірден таңдаңыз 👇")

print("✅ Бот Render-де іске қосылды")
bot.polling(non_stop=True)
