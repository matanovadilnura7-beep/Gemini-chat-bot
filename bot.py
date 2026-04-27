import telebot
from flask import Flask, request
import requests
import os

TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TOKEN:
    raise Exception("BOT_TOKEN topilmadi")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY topilmadi")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ChatGPT function
def ask_chatgpt(text):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=20)
        res = r.json()

        print("OPENAI RESPONSE:", res)

        if "choices" in res:
            return res["choices"][0]["message"]["content"]
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
        "👋 Salom! Men ChatGPT botman.\nSavol yoz 👇",
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

    javob = ask_chatgpt(message.text)

    bot.send_message(message.chat.id, javob)


# WEBHOOK
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@app.route('/', methods=['GET'])
def index():
    return "ChatGPT bot ishlayapti 🚀"


if __name__ == "__main__":
    url = os.environ.get("RENDER_EXTERNAL_URL")

    if url:
        bot.remove_webhook()
        bot.set_webhook(url=url)

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
