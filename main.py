import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7300225472:AAEtY2cPwsET309OVebfCRix4RNPmra9hJ8')

@bot.message_handler(content_types=['photo'])
def photo(message):
    mark = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на канал по боту', url='https://t.me/BotFather')
    mark.row(btn1)
    btn2 = types.InlineKeyboardButton('Перейти на сайт по боту', url='https://t.me/BotFather')
    btn3 = types.InlineKeyboardButton('Перейти на сайт по боту', url='https://t.me/BotFather')
    mark.row(btn2, btn3)
    bot.reply_to(message, 'Красивое фото!', reply_markup=mark)

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, f'<b>Привет! Сейчас вас зарегестрируем. Введите ваше имя </b>', parse_mode='html')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text.strip()
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(name, id) VALUES(?, ?)', (name, message.from_user.id))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['show'])
def show(message):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        bot.send_message(message.chat.id, f'ID: {row[0]}, Name: {row[1]}')
    conn.close()

@bot.message_handler()
def txt(message):
    if message.text.strip().lower() == 'привет':
        bot.send_message(message.chat.id, f'<b>Привет! {message.from_user.first_name}</b>', parse_mode='html')

bot.polling(none_stop=True)
