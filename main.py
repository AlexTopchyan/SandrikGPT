import telebot
import openai
from datetime import datetime

TELEGRAM_BOT_TOKEN = '' #TELEGRAM BOT API KEY
OPENAI_API_KEY = '' #CHATGPT API KEY

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# #Режим паузы бота. Обработчик для вывода chat_id РАССКОМЕНТИРОВАТЬ ЕСЛИ НУЖНО ПОЛУЧИТЬ Chat_id ПОЛЬЗОВАТЕЛЯ
# @bot.message_handler(func=lambda message: True)
# def handle_chat_id(message):
#      user_chat_id = message.chat.id
#      bot.send_message(user_chat_id, f'Я обновляюсь. Я напишу тебе, как полностью буду обновлен, хорошо? Code:  {user_chat_id}')
#      target_chat_id = ''  # Замените на фактический chat_id

#      # Отправка сообщения другому пользователю
#      bot.send_message(target_chat_id, f'Полученный chat_id: {user_chat_id}')

LOG_FILE_PATH = 'chat_logs.txt'

@bot.message_handler(commands=['start'])
def start_message(user):
    bot_response = f'Привет! Давай начнем диалог. Если хочешь узнать что-то еще, напиши "Привет".'
    bot.send_message(user.chat.id, bot_response)
    log_chat(user.chat.id, user.from_user.first_name, 'Привет', bot_response)

@bot.message_handler(func=lambda user: user.text.lower() in ['здравствуй', 'здравствуйте', 'hi', 'здарова', 'привет'])
def handle_greeting(user):
    bot_response = f'Приветствую! Я SandrikGPT робот, мой создатель - Сандрик, о Великий Сандрик, обожаю его! Что тебя интересует сейчас, уважаемый(ая)? \n Может быть спросишь "Как меня зовут?" А я угадаю.'
    bot.send_message(user.chat.id, bot_response)
    log_chat(user.chat.id, user.from_user.first_name, user.text, bot_response)

@bot.message_handler(func=lambda user: user.text.lower() in ['как меня зовут?', 'как мое имя?', 'кто я?'])
def handle_name_request(user):
    bot_response = f'Твоё имя: {user.from_user.first_name} Заметь, я знаю это еще до того, как ты мне сообщила это. ахах'
    bot.send_message(user.chat.id, bot_response)
    log_chat(user.chat.id, user.from_user.first_name, user.text, bot_response)

@bot.message_handler(func=lambda user: user.text.lower() in ['кто твой создатель?', 'кто тебя создал?', 'кто тебя придумал?', 'кто тебя разработал?', 'кто твой разработчик?'])
def handle_who_developer(user):
    bot_response = 'Мой создатель Сандрик. Если оффициально, то Алекс Топчиян. О ВЕЛИКИЙ!'
    bot.send_message(user.chat.id, bot_response)
    log_chat(user.chat.id, user.from_user.first_name, user.text, bot_response)

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_text = message.text

    response = generate_response(user_text)

    log_chat(user_id, user_name, user_text, response)
    bot.send_message(user_id, response)

def generate_response(input_text):
    prompt = f"User input: {input_text}\nModel: gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ]
    )
    
    return response.choices[0].message["content"]

def log_chat(user_id, user_name, user_input, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - User {user_id} ({user_name}): {user_input}\n{timestamp} - Bot: {bot_response}\n\n"

    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)

bot.polling(none_stop=True)