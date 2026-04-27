import telebot
import requests

TOKEN = "SENING_BOT_TOKEN"
API_KEY = "SENING_GEMINI_API"

bot = telebot.TeleBot(TOKEN)

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    response = requests.post(url, json=data)
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

@bot.message_handler(func=lambda message: True)
def reply(message):
    javob = ask_gemini(message.text)
    bot.reply_to(message, javob)

bot.polling()
