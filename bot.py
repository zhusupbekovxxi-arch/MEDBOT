import telebot
from telebot import types
import os

# --- Токен Render Environment-тен алынады ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- /start командасы ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Қызмет түрлері")
    btn2 = types.KeyboardButton("👨‍⚕️ Дәрігерлер")
    btn3 = types.KeyboardButton("📅 Жазылу")
    btn4 = types.KeyboardButton("💬 Кері байланыс")
    btn5 = types.KeyboardButton("ℹ️ Ақпарат")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    bot.send_message(
        message.chat.id,
        "👋 Сәлеметсіз бе! *МедЦентр.244* қабылдау бөлімі.\n"
        "Қажетті бөлімді таңдаңыз 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- Негізгі жауаптар ---
@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text == "📋 Қызмет түрлері":
        bot.send_message(
            message.chat.id,
            "🩺 *Біздің негізгі қызметтер:*\n"
            "• Терапевт — 8:00–20:00\n"
            "• Стоматолог — 9:00–19:00\n"
            "• Педиатр — 9:00–18:00\n"
            "• Қан талдауы, УДЗ, ЭКГ\n\n"
            "Төмендегі мәзір арқылы басқа бөлімді таңдаңыз 👇",
            parse_mode="Markdown"
        )

    elif message.text == "👨‍⚕️ Дәрігерлер":
        bot.send_message(
            message.chat.id,
            "👨‍⚕️ *Біздің дәрігерлер:*\n"
            "1. Д-р. Айжан Төлегенқызы — Терапевт\n"
            "2. Д-р. Ержан Нұрбекұлы — Стоматолог\n"
            "3. Д-р. Әлия Мұратқызы — Педиатр\n"
            "4. Д-р. Асқар Бекенов — УДЗ маманы",
            parse_mode="Markdown"
        )

    elif message.text == "📅 Жазылу":
        msg = bot.send_message(
            message.chat.id,
            "✍️ Жазылу үшін аты-жөніңізді жазыңыз:"
        )
        bot.register_next_step_handler(msg, ask_time)

    elif message.text == "💬 Кері байланыс":
        msg = bot.send_message(
            message.chat.id,
            "🗣 Пікіріңізді немесе ұсынысыңызды жазыңыз:"
        )
        bot.register_next_step_handler(msg, feedback_received)

    elif message.text == "ℹ️ Ақпарат":
        bot.send_message(
            message.chat.id,
            "🏥 *МедЦентр+ туралы:*\n"
            "• Мекенжай: Шиелі, Д.Смайлов көшесі 244\n"
            "• Байланыс: +7 (777) 123-45-67\n"
            "• Уақыты: 8:00–20:00 (күн сайын)\n\n"
            "📎 Instagram: @medcentr_plus\n"
            "🌐 Веб-сайт: medcentrplus.kz",
            parse_mode="Markdown"
        )

    else:
        bot.send_message(message.chat.id, "Төмендегі мәзірден таңдаңыз 👇")


# --- Жазылу функциясы ---
def ask_time(message):
    name = message.text
    msg = bot.send_message(
        message.chat.id,
        f"Рахмет, {name}!\n📅 Қай уақытқа жазылғыңыз келеді? (мысалы: ертең 15:00)"
    )
    bot.register_next_step_handler(msg, confirm_booking, name)

def confirm_booking(message, name):
    time = message.text
    bot.send_message(
        message.chat.id,
        f"✅ {name}, жазылуыңыз қабылданды!\nКүтілетін уақытыңыз: *{time}*\n"
        "Біздің оператор сізбен байланысады. 💬",
        parse_mode="Markdown"
    )

# --- Кері байланыс ---
def feedback_received(message):
    feedback = message.text
    bot.send_message(
        message.chat.id,
        "🙏 Пікіріңіз үшін рахмет! Біз міндетті түрде ескереміз."
    )
    # мұнда логқа немесе базаға сақтауға болады
    print(f"Пайдаланушы пікірі: {feedback}")

# --- Бот іске қосылады ---
print("✅ Бот Render-де іске қосылды")
bot.polling(non_stop=True)
