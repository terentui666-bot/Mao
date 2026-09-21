import os
import telebot
from openai import OpenAI

BOT_TOKEN = os.getenv('BOT_TOKEN')   
AI_KEY = os.getenv('AI_KEY')        

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_KEY
)
