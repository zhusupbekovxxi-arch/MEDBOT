import telebot
from telebot import types
from flask import Flask, request
import os
import openai

# --- 🔹 Токендер (Render Environment-тен алынады) ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 🔹 Тексеру үшін басты бет ---
@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!", 200

# --- 🔹 Webhook қабылдау ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# --- 🔹 /start командасы ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💊 Кеңес алу (AI)"))
    markup.add(types.KeyboardButton("📋 Қызмет түрлері"), types.KeyboardButton("📞 Байланыс / Жазылу"))
    bot.send_message(
        message.chat.id,
        "👋 Сәлем! Мен медициналық кеңесші ботпын.\n"
        "Симптомыңызды қысқаша жазыңыз — мен жалпы ақпараттық кеңес беремін.\n\n"
        "⚠️ *Ескерту:* Мен дәрігер емеспін, тек жалпы кеңес беремін.",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- 🔹 Кеңес алу батырмасы ---
@bot.message_handler(func=lambda m: m.text == "💊 Кеңес алу (AI)")
def ask_question(message):
    bot.send_message(message.chat.id, "Қандай симптом бар? Қысқаша түрде жазыңыз (мысалы: 'басым аурып тұр').")

# --- 🔹 Барлық басқа хабарламалар ---
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = (message.text or "").strip()

    # Егер мәзір батырмаларының біреуі болса — дайын жауаптар
    if text == "📋 Қызмет түрлері":
        bot.send_message(message.chat.id,
            "🩺 Біздің қызметтер:\n"
            "• Терапевт, стоматолог, педиатр\n"
            "• УДЗ, ЭКГ, қан талдауы және т.б.")
        return

    elif text == "📞 Байланыс / Жазылу":
        bot.send_message(message.chat.id,
            "📍 Мекенжай: Шиелі, Ғ.Мұратбаев 244\n"
            "📞 Телефон: +7 (777) 123-45-67
