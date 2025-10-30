import telebot
from telebot import types
from flask import Flask, request
import os

# 🔹 Токенді қоршаған ортадан алу (Render-де автоматты түрде)
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🔹 Тексеру үшін үй беті
@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!", 200

# 🔹 Webhook арқылы Telegram жаңартуларын қабылдау
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# 🔹 /start командасы — басты мәзірді көрсету
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

# 🔹 Негізгі жауаптар
@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text == "📋 Қызмет түрлері":
        bot.send_message(message.chat.id,
            "🩺 Біздің қызметтер:\n"
            "• Терапевт — 8:00–20:00\n"
            "• Стоматолог — 9:00–19:00\n"
            "• УДЗ, ЭКГ, қан талдауы\n"
            "• Балалар дәрігері (педиатр)\n"
            "• Дерматолог, офтальмолог және т.б.")
    
    elif message.text == "📞 Байланыс / Жазылу":
        bot.send_message(message.chat.id,
            "📍 Мекенжай: Шиелі, Ғ.Мұратбаев 244\n"
            "📞 Телефон: +7 (777) 123-45-67\n"
            "🕒 Уақыты: 8:00–20:00\n\n"
            "Онлайн жазылу үшін хабарласыңыз 👇")

    elif message.text == "💊 Препараты / Дәрігер кеңесі":
        bot.send_message(message.chat.id,
            "💊 Біздің дәрігерлер заманауи препараттар мен ем тәсілдері туралы кеңес береді.\n"
            "Кеңес алу үшін қабылдауға жазылыңыз.")

    elif message.text == "📰 Жаңалықтар / Акциялар":
        bot.send_message(message.chat.id,
            "📰 Соңғы жаңалықтар мен жеңілдіктер:\n"
            "• 1 қараша — тегін қан талдауы күні 🩸\n"
            "• Стоматологияда 20% жеңілдік 💎\n\n"
            "Толығырақ ақпарат алу үшін операторға хабарласыңыз 📞")

    else:
        bot.send_message(message.chat.id, "Төмендегі мәзірден таңдаңыз 👇")

# 🔹 Webhook орнату және Flask қосу
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    render_url = os.environ.get("RENDER_EXTERNAL_URL")

    # ✅ HTTPS бар-жоғын тексеру
    webhook_url = f"{render_url}/{TOKEN}" if render_url.startswith("https://") else f"https://{render_url}/{TOKEN}"

    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

    print(f"✅ Webhook орнатылды: {webhook_url}")
    app.run(host="0.0.0.0", port=port)
