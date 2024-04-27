import telebot
from telebot import types
from Bitrix24 import create_lead, assign_lead_to_employee, get_employee_id, update_lead_stage
import re

API_TOKEN = '7011505654:AAH2ZqjE_Tep8PU31NcPXi4Sm-5_eOD6Eg0'
bot = telebot.TeleBot(API_TOKEN)

user_state = {}
user_data = {}


QUERY, PHONE, NAME, EMAIL = range(4)

def valid_email(email):
    pattern = r'^[a-z0-9\.\-_]+@[a-z0-9\-_]+\.[a-z]{2,}$'
    return re.match(pattern, email) is not None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_state[message.chat.id] = QUERY
    bot.reply_to(message, 'Здравствуйте, напишите ваш запрос.')

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def collect_info(message):
    chat_id = message.chat.id
    state = user_state[chat_id]

    if state == QUERY:
        user_data[chat_id] = {'query': message.text}
        user_state[chat_id] = PHONE
        bot.reply_to(message, 'Спасибо! Теперь отправьте ваш номер телефона.')
    elif state == PHONE:
        user_data[chat_id]['phone'] = message.text
        user_state[chat_id] = NAME
        bot.reply_to(message, 'Теперь напишите ваше ФИО.')
    elif state == NAME:
        user_data[chat_id]['name'] = message.text
        user_state[chat_id] = EMAIL
        bot.reply_to(message, 'Почти закончили, отправьте вашу почту.')
    elif state == EMAIL:
        email = message.text
        if valid_email(email):
            user_data[chat_id]['email'] = email
            user_state.pop(chat_id)
            response = create_lead(
                user_data[chat_id]['name'],
                user_data[chat_id]['phone'],
                user_data[chat_id]['email'],
                user_data[chat_id]['query']
            )

            if 'result' in response:
                lead_id = response['result']
                employee_id = get_employee_id(7)
                if employee_id:
                    assign_response = assign_lead_to_employee(lead_id, employee_id)
                    if 'result' in assign_response:
                        stage_response = update_lead_stage(lead_id, 'UC_J7YV5P')
                        if 'result' in stage_response:
                            reply_message = f"{user_data[chat_id]['name']}, спасибо, мы получили ваши данные. Ваш запрос теперь в стадии 'Заполнил форму'. Ваш идентификатор лида: {lead_id}."
                        else:
                            reply_message = "Ошибка при обновлении стадии лида."
                    else:
                        reply_message = "Ошибка при назначении лида сотруднику."
                else:
                    reply_message = "Не удалось получить ID сотрудника."
            else:
                error_description = response.get('error_description', 'No error description provided.')
                reply_message = f"Ошибка при создании лида: {error_description}"
            bot.reply_to(message, reply_message)
        else:
            bot.reply_to(message, "Введенный email некорректен. Пожалуйста, введите правильный email.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "Для начала введите команду /start.")

bot.infinity_polling()
