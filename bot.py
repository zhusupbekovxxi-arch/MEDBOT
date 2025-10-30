import telebot
from telebot import types
from flask import Flask, request
import os
import openai

# --- 🔹 Токендерді алу (Render environment-тен) ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 🔹 Үй беті ---
@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!", 200

# --- 🔹 Webhook жаңартуларын қабылдау ---
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
    markup.add(types.KeyboardButton("📰 Жаңалықтар / Акциялар"))
    bot.send_message(
        message.chat.id,
        "👋 Сәлеметсіз бе! *МедЦентр+* қабылдау бөлімі.\n"
        "Симптомыңызды немесе сұрағыңызды жазыңыз — бот жалпы кеңес береді.\n"
        "(Ескерту: бұл тек ақпараттық көмек, нақты диагноз үшін дәрігерге жүгініңіз.)",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- 🔹 Батырмалар логикасы ---
@bot.message_handler(func=lambda m: m.text == "📋 Қызмет түрлері")
def services(message):
    bot.send_message(message.chat.id,
        "🩺 Біздің қызметтер:\n"
        "• Терапевт — 8:00–20:00\n"
        "• Стоматолог — 9:00–19:00\n"
        "• УДЗ, ЭКГ, қан талдауы\n"
        "• Педиатр, дерматолог және офтальмолог")

@bot.message_handler(func=lambda m: m.text == "📞 Байланыс / Жазылу")
def contact(message):
    bot.send_message(message.chat.id,
        "📍 Мекенжай: Шиелі, Ғ.Мұратбаев 244\n"
        "📞 Телефон: +7 (777) 123-45-67\n"
        "🕒 Уақыты: 8:00–20:00\n\n"
        "Онлайн жазылу үшін хабарласыңыз 👇")

@bot.message_handler(func=lambda m: m.text == "📰 Жаңалықтар / Акциялар")
def news(message):
    bot.send_message(message.chat.id,
        "📰 Соңғы жаңалықтар мен жеңілдіктер:\n"
        "• 1 қараша — тегін қан талдауы 🩸\n"
        "• Стоматологияда 20% жеңілдік 💎\n\n"
        "Толығырақ ақпарат алу үшін операторға хабарласыңыз 📞")

@bot.message_handler(func=lambda m: m.text == "💊 Кеңес алу (AI)")
def ask_ai(message):
    bot.send_message(message.chat.id, "Қандай симптом бар? Қысқа түрде жазыңыз (мысалы: 'басым аурып тұр').")

# --- 🔹 Барлық басқа мәтіндер — ІІ кеңесі ---
@bot.message_handler(func=lambda m: True)
def handle_ai(message):
    text = (message.text or "").strip()
    if len(text) < 3:
        bot.send_message(message.chat.id, "Өтініш, симптомды қысқаша әрі нақты жазыңыз.")
        return

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                 "Сен медициналық кеңесші ботсың. Пайдаланушыға тек жалпы, қауіпсіз кеңес бер. "
                 "Диагноз қойма және нақты дәрі-дәрмек жазба. Егер симптом қауіпті болса "
                 "(мысалы: қан кету, тыныс алу қиындығы, есінен тану) — дереу жедел жәрдемге баруды ұсын."},
                {"role": "user", "content": text}
            ],
            max_tokens=350,
            temperature=0.3,
        )
        answer = completion["choices"][0]["message"]["content"].strip()
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        print("OpenAI Error:", e)
        bot.send_message(message.chat.id, "⚠️ Кеңес алу сәтсіз. Кейінірек қайталап көріңіз.")

# --- 🔹 Webhook орнату және қосу ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if render_url.startswith("https://"):
        webhook_url = f"{render_url}/{TOKEN}"
    else:
        webhook_url = f"https://{render_url}/{TOKEN}"

    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

    print("✅ Webhook set to:", webhook_url)
    app.run(host="0.0.0.0", port=port)
