import telebot
from flask import Flask, request
import requests
import os

TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("GEMINI_API")

if not TOKEN or not API_KEY:
    raise RuntimeError("BOT_TOKEN yoki GEMINI_API topilmadi (Environment’da qo‘shing)")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": text}]}]}
    r = requests.post(url, json=data, timeout=20)
    try:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ Xatolik yuz berdi"

@bot.message_handler(commands=['start'])
def start(m):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🤖 AI chat", "ℹ️ Help")
    bot.send_message(m.chat.id, "👋 Salom!", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.send_message(m.chat.id, "⏳ Kuting...")
    bot.send_message(m.chat.id, ask_gemini(m.text))

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
