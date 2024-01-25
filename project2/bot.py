import json
from TOKEN import TOKEN
import telebot
from telebot import types
from location_num_1 import lobby, start, help

bot = telebot.TeleBot(TOKEN)

STATE = {}

# Функция для отправи фото и текста с кнопками
def get_current_question_info(message):
    current_question = STATE[message.chat.id]
    with open(f'photo_location/{current_question["photo"]}', 'rb') as f:
        bot.send_photo(message.chat.id, f)
    markup = create_inline_keyboard(current_question['answers'].keys())
    bot.send_message(message.chat.id, current_question['text'], reply_markup=markup)


# Функция для КНОПАК
def create_inline_keyboard(buttons_text):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for button_text in buttons_text:
        buttons.append(types.InlineKeyboardButton(button_text, callback_data=button_text))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, start)


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, help)

# Функция загружает в STATE пользователя и отпровляет текст с фото
@bot.message_handler(commands=['go'])
def go_handler(message):
    STATE[message.chat.id] = lobby[0]
    get_current_question_info(message)

# Функция для обработки нажатие кнопки
@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback: types.CallbackQuery):
    curent_user_question = STATE[callback.message.chat.id]
    answers = curent_user_question['answers']
    STATE[callback.message.chat.id] = answers[callback.data]
    if callback.data == 'Начать занаво':
        STATE[callback.message.chat.id] = lobby[0]
    elif callback.data == 'Назад' or callback.data == 'Продолжить':
        STATE[callback.message.chat.id] = lobby[answers[callback.data]]
    else:
        STATE[callback.message.chat.id] = answers[callback.data]
    get_current_question_info(callback.message)

    bot.delete_message(callback.message.chat.id, callback.message.id)


bot.polling()