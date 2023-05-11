import calendar

import telebot
import threading
import time
from telebot import types

from server.config import TOKEN

from server.models import *
from server.models import RequestTime

bot = telebot.TeleBot(TOKEN)

reg_users = {}

russification_day_week = {
    'monday': 'Понедельник',
    'tuesday': 'Вторник',
    'wednesday': 'Среда',
    'thursday': 'Четверг',
    'friday': 'Пятница',
    'saturday': 'Суббота',
    'sunday': 'Воскресенье',
}


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
        bot.send_message(chat_id, 'Выдаю вам клавиатуру ⌨️', reply_markup=get_standart_markup())
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
    elif call.data.count('minute_'):
        user = User.get_or_none(User.telegram == chat_id)
        date_today = datetime.date.today()
        request_time = RequestTime.select().where(
            RequestTime.day == date_today,
            RequestTime.user == user,
        )
        print(len(request_time))
        if not request_time:
            return
        request_time = request_time[-1]
        minute = call.data.split('_')[-1]
        request_time.amount = minute
        request_time.save()
        bot.edit_message_text(f'✅ Вы успешно увеличили лимит для текущего дня на: {minute} минут!', chat_id=chat_id,
                              message_id=call.message.message_id)


def get_standart_markup(block_status=False):
    markup = types.ReplyKeyboardMarkup()
    button_statistic = types.KeyboardButton('📊 Статистика')
    button_limits = types.KeyboardButton('🕒 Лимиты')
    button_time_now = types.KeyboardButton('🧑‍💻 Использовано')
    if block_status:
        button_block = types.KeyboardButton('✅ Разблокировать')
    else:
        button_block = types.KeyboardButton('⛔️ Заблокировать')
    markup.add(button_statistic)
    markup.add(button_limits, button_time_now)
    markup.add(button_block)
    return markup


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
        date_today = datetime.date.today()
        for request_time in RequestTime.select().where(
                RequestTime.is_send == False,
                RequestTime.day == date_today,
        ):
            keyboard = types.InlineKeyboardMarkup()
            minute_5 = types.InlineKeyboardButton(text='5', callback_data=f'minute_5')
            minute_15 = types.InlineKeyboardButton(text='15', callback_data=f'minute_15')
            minute_30 = types.InlineKeyboardButton(text='30', callback_data=f'minute_30')
            minute_60 = types.InlineKeyboardButton(text='60', callback_data=f'minute_60')
            minute_90 = types.InlineKeyboardButton(text='90', callback_data=f'minute_90')
            minute_120 = types.InlineKeyboardButton(text='120', callback_data=f'minute_120')
            keyboard.add(minute_5, minute_15, minute_30)
            keyboard.add(minute_60, minute_90, minute_120)
            bot.send_message(
                request_time.user.telegram,
                'Запрос дополнительного времени.\n Укажите, сколько минут вы хотите добавить (или просто проигнорируйте это сообщение).',
                reply_markup=keyboard)
            request_time.is_send = True
            request_time.save()
        time.sleep(1.5)


@bot.message_handler(content_types=['text'])
def keyboard_handler(message):
    commands = {
        '📊 Статистика': statistic,
        '🕒 Лимиты': limit,
        '🧑‍💻 Использовано': time_amount,
        '⛔️ Заблокировать': block,
        '✅ Разблокировать': block,
    }
    if commands.get(message.text):
        commands[message.text](message)


def number_of_days(date_1, date_2):
    return (date_2 - date_1).days


def correct_word(number, lst):
    assert len(lst) == 3
    units = number % 10
    tens = (number // 10) % 10
    if tens == 1:
        return lst[0]
    if units in [0, 5, 6, 7, 8, 9]:
        return lst[0]
    if units == 1:
        return lst[1]
    if units in [2, 3, 4]:
        return lst[2]


def statistic(message):
    chat_id = message.chat.id
    user = User.get_or_none(User.telegram == chat_id)
    if not user:
        bot.send_message(chat_id, 'Вы авторизованы!')
        return
    session = TimeDaySession.select().where(TimeDaySession.user == user)
    result_str = '📊 Статистика использования компьютера за последнюю неделю:\n\n'
    for i in session:
        if number_of_days(i.day, datetime.date.today()) < 7:
            day = calendar.day_name[i.day.weekday()].lower()
            hour, minute = get_humanize_time(i.time)
            result_str += f'{russification_day_week[day.lower()]} - {hour} {minute}\n'
    bot.send_message(chat_id, result_str)


def get_humanize_time(time_):
    _hour = int(time_.split(":")[0])
    hour = f'{_hour} {correct_word(_hour, ("часов", "час", "часа",))}'
    _minute = int(time_.split(":")[1])
    minute = f'{_minute} {correct_word(_minute, ("минут", "минута", "минуты",))}'
    return hour, minute


def limit(message):
    chat_id = message.chat.id
    user = User.get_or_none(User.telegram == chat_id)
    if not user:
        bot.send_message(chat_id, 'Вы авторизованы!')
        return
    limit = ControlDate.get_or_none(ControlDate.user == user)
    if not limit:
        bot.send_message(chat_id, 'Вы ещё не создали лимиты!')
    result_str = 'Лимиты использования компьютера:\n\n'
    for i in russification_day_week:
        hour, minute = get_humanize_time(getattr(limit, i))
        if hour.count('23') and minute.count('59'):
            result_str += f'{russification_day_week[i]} - нет лимита\n'
        else:
            result_str += f'{russification_day_week[i]} - {hour} {minute}\n'
    bot.send_message(chat_id, result_str)


def time_amount(message):
    chat_id = message.chat.id
    user = User.get_or_none(User.telegram == chat_id)
    if not user:
        bot.send_message(chat_id, 'Вы авторизованы!')
        return
    limit = ControlDate.get_or_none(ControlDate.user == user)
    if not limit:
        bot.send_message(chat_id, 'Вы ещё не создали лимиты!')
        return
    today = datetime.date.today()
    day = calendar.day_name[today.weekday()].lower()
    limit = getattr(limit, day)
    session = TimeDaySession.get_or_none(TimeDaySession.user == user, TimeDaySession.day == today)
    if not session:
        hour, minute = get_humanize_time(limit.time)
        bot.send_message(chat_id, f'⏳ Осталось {hour} {minute} компьютерного времени')
        return
    hour_limit = int(limit.split(':')[0])
    minute_limit = int(limit.split(':')[1])

    hour_session = int(session.time.split(':')[0])
    minute_session = int(session.time.split(':')[1])

    hour = '0 часов'
    minute = '0 минут'

    if hour_limit - hour_session > 0:
        hour, _ = get_humanize_time(f'{hour_limit - hour_session}:1')
    if minute_limit - minute_session > 0:
        _, minute = get_humanize_time(f'1:{minute_limit - minute_session}')
    hour_session, minute_session = get_humanize_time(f'{hour_session}:{minute_session}')
    bot.send_message(chat_id,
                     f'Использовано {hour_session} {minute_session}.\nОсталось {hour} {minute} компьютерного времени')


def block(message):
    chat_id = message.chat.id
    user = User.get_or_none(User.telegram == chat_id)
    ban = Ban.get_or_create(user=user)
    if ban[1]:
        bot.send_message(chat_id, f'❌ Компьютер заблокирован!', reply_markup=get_standart_markup(True))
    else:
        ban[0].delete_instance()
        bot.send_message(chat_id, f'✅ Компьютер разблокирован!', reply_markup=get_standart_markup())


if __name__ == '__main__':
    thread = threading.Thread(target=check_confirm_login)
    thread.start()
    print('Бот запущен')
    bot.infinity_polling()
