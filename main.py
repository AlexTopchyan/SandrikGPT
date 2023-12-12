import telebot
import openai
from datetime import datetime

TELEGRAM_BOT_TOKEN = '5810666729:AAFC-3KWEWrOUUSsMr0ywCx36YeFw3NpQco'
OPENAI_API_KEY = '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'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# #Режим паузы бота. Обработчик для вывода chat_id РАССКОМЕНТИРОВАТЬ ЕСЛИ НУЖНО ПОЛУЧИТЬ Chat_id ПОЛЬЗОВАТЕЛЯ
# @bot.message_handler(func=lambda message: True)
# def handle_chat_id(message):
#      user_chat_id = message.chat.id
#      bot.send_message(user_chat_id, f'Я обновляюсь. Я напишу тебе, как полностью буду обновлен, хорошо? Code:  {user_chat_id}')
#      target_chat_id = '657745373'  # Замените на фактический chat_id

#      # Отправка сообщения другому пользователю
#      bot.send_message(target_chat_id, f'Полученный chat_id: {user_chat_id}')

# Дополнительные настройки
LOG_FILE_PATH = 'chat_logs.txt'  # Укажите путь к файлу логов

# Шаблонные ответы
@bot.message_handler(commands=['start'])
def start_message(user):
    bot.send_message(user.chat.id, 'Привет! Давай начнем диалог. Если хочешь узнать что-то еще, напиши "Привет".')

@bot.message_handler(func=lambda user: user.text.lower() in ['как меня зовут?', 'как мое имя?', 'кто я?'])
def handle_name_request(user):
    bot.send_message(user.chat.id, f'Твоё имя: {user.from_user.first_name} Заметь, я знаю это еще до того, как ты мне сообщила это. ахах')
    bot.send_message(user.chat.id, f'Теперь задавай любые вопросы. Только прошу тебя, задавай их максимально точно и понятно.')
    bot.send_message(user.chat.id, f'Мой создатель обучил меня так, что я смогу покорить все вершины! Ну вперёд {user.from_user.first_name}, я готов поговорить с тобой! \n Может тебе интересно, кто меня приудмал?')

@bot.message_handler(func=lambda user: user.text.lower() in ['кто твой создатель?', 'кто тебя создал?', 'кто тебя придумал?', 'кто тебя разработал?', 'кто твой разработчик?'])
def handle_who_developer(user):
    bot.send_message(user.chat.id, 'Мой создатель Сандрик. Если оффициально, то Алекс Топчиян. О ВЕЛИКИЙ!')

@bot.message_handler(func=lambda user: user.text.lower() in ['здравствуй', 'здравствуйте', 'hi', 'здарова', 'привет'])
def handle_greeting(user):
    bot.send_message(user.chat.id, f'Приветствую! Я SandrikGPT робот, мой создатель - Сандрик, о Великий Сандрик, обожаю его! Что тебя интересует сейчас, уважаемый(ая)? \n Может быть спросишь "Как меня зовут?" А я угадаю.')

# ChatGPT Integration
@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    user_id = message.from_user.id
    user_text = message.text

    # Вызов чат-модели GPT-3.5-turbo
    response = generate_response(user_text)

    # Сохранение переписки в файл
    log_chat(user_id, user_text, response)

    # Отправка ответа пользователю
    bot.send_message(user_id, response)

def generate_response(input_text):
    # Вызов чат-модели GPT-3.5-turbo с использованием OpenAI API
    prompt = f"User input: {input_text}\nModel: gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ]
    )
    
    return response.choices[0].message["content"]

def log_chat(user_id, user_input, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - User {user_id}: {user_input}\n{timestamp} - Bot: {bot_response}\n\n"

    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)

# Запуск бота
bot.polling(none_stop=True)