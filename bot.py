import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# /start командасы
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Қызмет түрлері")
    btn2 = types.KeyboardButton("📞 Байланыс / Жазылу")
    btn3 = types.KeyboardButton("💊 Препараты / Дәрігер кеңесі")
    btn4 = types.KeyboardButton("📰 Жаңалықтар / Акциялар")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "👋 Сәлеметсіз бе! *МедЦентр+* қабылдау бөлімі.\n"
        "Қажетті бөлімді таңдаңыз 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )

# Мәзірдегі жауаптар
@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text == "📋 Қызмет түрлері":
        bot.send_message(message.chat.id, "🩺 Біздің негізгі қызметтер:\n• Терапевт — 8:00–20:00\n• Стоматолог — 9:00–19:00\n• Қан талдауы, УДЗ, ЭКГ")
    elif message.text == "📞 Байланыс / Жазылу":
        bot.send_message(message.chat.id, "📍 Шиелі Ғ.Мұратбаев 244\n📞 +7 (777) 123-45-67\n🕒 8:00–20:00")
    elif message.text == "💊 Препараты / Дәрігер кеңесі":
        bot.send_message(message.chat.id, "💊 Дәрігер кеңестері мен препараттар туралы ақпарат алуға болады.")
    elif message.text == "📰 Жаңалықтар / Акциялар":
        bot.send_message(message.chat.id, "📰 Соңғы жаңалықтар мен акциялар:\n• 1 қараша — тегін тексеру күні\n• 20% жеңілдік стоматологияда")
    else:
        bot.send_message(message.chat.id, "Төмендегі мәзірден таңдаңыз 👇")

# Telegram серверлерінен жаңалық қабылдау (Webhook)
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RENDER_EXTERNAL_URL')}/{TOKEN}")
    app.run(host="0.0.0.0", port=port)
