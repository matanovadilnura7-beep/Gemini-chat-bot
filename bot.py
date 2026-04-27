import telebot
from flask import Flask, request
import requests
import os

TOKEN = os.environ.get("8717105037:AAGHh9ucJCqTAAS4uKuzJOFKDzYQ0_UPBb")
API_KEY = os.environ.get("AIzaSyArww8FWEtiXfCEQwd1eyd3Z4D5L_0sVz0")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Gemini function
def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    response = requests.post(url, json=data)
    
    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ Xatolik yuz berdi"

# START BUTTONS
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("🤖 AI bilan gaplashish")
    btn2 = telebot.types.KeyboardButton("ℹ️ Yordam")
    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        "👋 Salom! Men AI botman.\nTugmalardan birini tanla:",
        reply_markup=markup
    )

# HELP
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def help_msg(message):
    bot.send_message(message.chat.id, "✍️ Menga istalgan savol yoz — men AI orqali javob beraman!")

# AI CHAT
@bot.message_handler(func=lambda m: True)
def chat(message):
    bot.send_message(message.chat.id, "⏳ Kuting...")
    answer = ask_gemini(message.text)
    bot.send_message(message.chat.id, answer)

# WEBHOOK
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/', methods=['GET'])
def index():
    return "Bot ishlayapti 🚀"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL"))
    app.run(host="0.0.0.0", port=10000)
