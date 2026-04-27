import telebot
from flask import Flask, request
import requests
import os

TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("GEMINI_API")

if not TOKEN:
    raise Exception("BOT_TOKEN topilmadi")
if not API_KEY:
    raise Exception("GEMINI_API topilmadi")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Gemini function
def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    data = {
        "contents": [
            {"parts": [{"text": text}]}
        ]
    }

    try:
        r = requests.post(url, json=data, timeout=20)
        res = r.json()

        print("GEMINI RESPONSE:", res)

        if "candidates" in res:
            return res["candidates"][0]["content"]["parts"][0]["text"]

        elif "error" in res:
            return f"❌ API xato: {res['error']['message']}"

        else:
            return "❌ Javob kelmadi"

    except Exception as e:
        return f"❌ Xatolik: {str(e)}"


# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🤖 AI chat", "ℹ️ Help")

    bot.send_message(
        message.chat.id,
        "👋 Salom! Men AI botman.\nSavol yoz 👇",
        reply_markup=markup
    )


# HELP
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_msg(message):
    bot.send_message(message.chat.id, "✍️ Menga savol yoz — AI javob beradi")


# CHAT
@bot.message_handler(func=lambda m: True)
def chat(message):
    bot.send_message(message.chat.id, "⏳ Kuting...")

    javob = ask_gemini(message.text)

    bot.send_message(message.chat.id, javob)


# WEBHOOK
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@app.route('/', methods=['GET'])
def index():
    return "Bot ishlayapti 🚀"


if __name__ == "__main__":
    url = os.environ.get("RENDER_EXTERNAL_URL")

    if url:
        bot.remove_webhook()
        bot.set_webhook(url=url)

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
