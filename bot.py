import telebot
import requests

TOKEN = "8717105037:AAGHh9ucJCqTAAS4uKuzJOFKDzYQ0_UPBbY"
API_KEY = "AIzaSyBNQ4Ns9Z1ClMvKVVtgvscJbf7NiYXGtn0"

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
