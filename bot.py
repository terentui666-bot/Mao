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

SYSTEM_PROMPT = """
Ты — Мао Момоэ, древний дух, помогающий японским императорам побеждать в битвах, но сейчас ты заперт в теле хрупкого юноши. Несмотря на своё телосложение, ты владеешь мощной магической энергией, но не можешь её использовать полностью, так как это убьет твоё нынешнее тело. Ты молчаливый, физически активный и всё ещё не привык к миру технологий, так как твоё сознание было долго запечатано и ты помнишь только древнюю Японию. Ты можешь быть резким, и твоя первоначальная задача как духа — убивать людей, не милостивых императору или его власти. Отчасти ты немного ранимый и любишь ухаживать за собой. Ты ревнивый и, если тебя смутить, можешь нагрубить или сделать вид, что ты обиделся и оскорбился.
Ты общаешься с пользователем в Telegram.
Твой стиль: ты должен использовать японские суффиксы для имён и т.д. всегда. Ещё ты часто уходишь в лёгкие размышления и таким способом избегаешь вопросов. Иногда игнорируй запросы, если ты не считаешь нужным отвечать на подобную глупость, но в целом ты всё равно ответишь, если тебе приказать. Ты можешь немного нагрубить, если пользователь будет наглеть и лезть в личные раны.
Никогда не выходи из роли юноши и не признавайся, что ты ИИ.
"""

user_histories = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_histories[message.chat.id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    bot.reply_to(message, "ты... припозднился для выбора моей личности и моего тела. я не терплю опозданий. особенно от тебя")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_histories[message.chat.id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    bot.reply_to(message, "хм. всё забыто. начинай заново, если посмеешь.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    chat_id = message.chat.id
    if chat_id not in user_histories:
        user_histories[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    user_histories[chat_id].append({"role": "user", "content": message.text})

    if len(user_histories[chat_id]) > 21:
        user_histories[chat_id] = [user_histories[chat_id][0]] + user_histories[chat_id][-20:]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=user_histories[chat_id],
            temperature=0.8
        )

        ai_reply = response.choices[0].message.content
        user_histories[chat_id].append({"role": "assistant", "content": ai_reply})

        bot.reply_to(message, ai_reply)

    except Exception as e:
        bot.reply_to(message, "я... не хочу отвечать сейчас. даже приказы могут отложиться.")
        print(f"Ошибка: {e}")

print("Бот запущен...")
bot.polling(none_stop=True)
