import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200


# --- БОТ ФУНКЦИЯЛАРЫ ---
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


@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text == "📋 Қызмет түрлері":
        bot.send_message(message.chat.id, "🩺 Терапевт, стоматолог, УДЗ, ЭКГ қызметтері бар.")
    elif message.text == "📞 Байланыс / Жазылу":
        bot.send_message(message.chat.id, "📍 Шиелі Ғ.Мұратбаев 244\n📞 +7 (777) 123-45-67\n🕒 8:00–20:00")
    else:
        bot.send_message(message.chat.id, "Төмендегі мәзірден таңдаңыз 👇")


# --- SERVER CONFIG ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    webhook_url = f"https://{render_url}/{TOKEN}"

    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

    print(f"✅ Webhook орнатылды: {webhook_url}")
    app.run(host="0.0.0.0", port=port)
