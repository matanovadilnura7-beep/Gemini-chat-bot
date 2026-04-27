import telebot
import requests

TOKEN = "8717105037:AAGHh9ucJCqTAAS4uKuzJOFKDzYQ0_UPBbY"
API_KEY = "AIzaSyArww8FWEtiXfCEQwd1eyd3Z4D5L_0sVz0"

bot = telebot.TeleBot(TOKEN)

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    response = requests.post(url, json=data)
    
    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Xatolik yuz berdi (API javob bermadi)"

@bot.message_handler(func=lambda message: True)
def reply(message):
    javob = ask_gemini(message.text)
    bot.reply_to(message, javob)

bot.polling(none_stop=True)
