import telebot
import threading
import time
from telebot import types

from server.config import TOKEN

from server.models import *

bot = telebot.TeleBot(TOKEN)

reg_users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    if User.get_or_none(User.telegram == message.chat.id):
        get_user_data = types.InlineKeyboardButton(text='Напомнить данные', callback_data='get_user_data')
        keyboard.add(get_user_data)
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы 😊', reply_markup=keyboard)
        return
    message_start = BotText.get_or_none(tag='Начало').text
    yes = types.InlineKeyboardButton(text='Конечно 😀', callback_data='reg_yes')
    keyboard.add(yes)
    if not message_start:
        message_start = 'Добрый день, давайте зарегистрируемся'
    bot.send_message(message.chat.id, message_start, reply_markup=keyboard)


def enter_login(message):
    reg_users[message.chat.id] = {
        'login': message.text,
    }
    message_start = BotText.get_or_none(tag='Регистрации ввод пароля').text
    if not message_start:
        message_start = 'Введите пароль:'
    bot.send_message(message.chat.id, message_start)
    bot.register_next_step_handler(message, enter_password)


def enter_password(message):
    reg_users[message.chat.id]['password'] = message.text
    message_start = BotText.get_or_none(tag='Регистрация уточнение данных').text
    if not message_start:
        message_start = 'Всё верно?'
    message_start += f'\nЛогин: {reg_users[message.chat.id]["login"]}\nПароль: {reg_users[message.chat.id]["password"]}'
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='✅ Да, всё верно', callback_data='reg_check_yes')
    no = types.InlineKeyboardButton(text='❌ Нет, поправить', callback_data='reg_check_no')
    keyboard.add(yes, no)
    bot.send_message(message.chat.id, message_start, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    msg_by_callback(call.data, chat_id)
    if call.data in ('reg_check_no', 'reg_yes',):
        bot.register_next_step_handler(call.message, enter_login)
    elif call.data == 'reg_check_yes':
        login = reg_users[chat_id]['login']
        password = reg_users[chat_id]['password']
        User.create(mac='-1', telegram=chat_id, login=login, password=password)
    elif call.data == 'get_user_data':
        user = User.get_or_none(User.telegram == chat_id)
        bot.send_message(chat_id, f'🤫 Данные для входа:\nЛогин: {user.login}\nПароль: {user.password}')
    elif call.data.count('this_i_') or call.data.count('this_no_i_'):
        mac = call.data.split('_')[-1]
        user = User.get_or_none(mac=mac)
        if not user:
            return
        conf = ConfirmLogin.get_or_none(ConfirmLogin.user == user)
        if not conf:
            bot.send_message(chat_id, f'⚠️ Вход уже подтверждён!')
            return
        if call.data.count('this_i_'):
            conf.status = 1
            conf.save()
            bot.send_message(chat_id, f'✅ Вы подтвердили вход!')
            return
        conf.status = 0
        conf.save()
        bot.send_message(chat_id, f'🚫 Мы запретили вход!')


def msg_by_callback(callback_data: str, chat_id: int) -> None:
    actions = {
        'reg_yes': {
            'tag': 'Регистрация ввод логина',
            'default': 'Введите логин:',
        },
        'reg_check_yes': {
            'tag': 'Регистрация конец',
            'default': 'Вы успешно авторизованы!',
        },
        'reg_check_no': {
            'tag': 'Регистрация данные неверны',
            'default': 'Хорошо, начнём заново.\nВведите логин:',
        },
    }
    action = actions.get(callback_data)
    if not action:
        return
    message_start = BotText.get_or_none(tag=action['tag']).text
    if not message_start:
        message_start = action['default']
    bot.send_message(
        chat_id,
        message_start,
        reply_markup=types.ReplyKeyboardRemove()
    )


def check_confirm_login():
    while True:
        for login_confirm in ConfirmLogin.select().where(ConfirmLogin.status == -1):
            keyboard = types.InlineKeyboardMarkup()
            this_i = types.InlineKeyboardButton(text='✅ Это я', callback_data=f'this_i_{login_confirm.user.mac}')
            this_no_i = types.InlineKeyboardButton(text='❌ Это не я',
                                                   callback_data=f'this_no_i_{login_confirm.user.mac}')
            keyboard.add(this_i, this_no_i)
            bot.send_message(login_confirm.user.telegram, 'Подтвердите вход', reply_markup=keyboard)
            login_confirm.status = -2
            login_confirm.save()
        time.sleep(1.5)


if __name__ == '__main__':
    thread = threading.Thread(target=check_confirm_login)
    thread.start()
    print('Бот запущен')
    bot.infinity_polling()
