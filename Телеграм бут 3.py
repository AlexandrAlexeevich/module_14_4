import sqlite3

def initiate_db():
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')
        conn.commit()

def get_all_products():
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, price FROM Products')
        return cursor.fetchall()

import telebot
from telebot import types
from crud_functions import initiate_db, get_all_products

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных и добавление тестовых данных
initiate_db()

def populate_db():
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Product1', 'описание 1', 100)")
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Product2', 'описание 2', 200)")
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Product3', 'описание 3', 300)")
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Product4', 'описание 4', 400)")
        conn.commit()

# Вызов функции для заполнения базы данных (первый запуск кода)
populate_db()

# Создание главной клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buy_button = types.KeyboardButton("Купить")
main_keyboard.add(buy_button)

# Функция для отправки списка продуктов
def get_buying_list(message):
    products = get_all_products()

    for product in products:
        title, description, price = product
        bot.send_message(message.chat.id,
                         f'Название: {title} | Описание: {description} | Цена: {price}')
        # Здесь замените 'image_url' на фактический URL изображения продукта
        # bot.send_photo(message.chat.id, 'image_url')

    # Создание Inline клавиатуры
    inline_keyboard = types.InlineKeyboardMarkup()
    for product in products:
        title, _, _ = product
        button = types.InlineKeyboardButton(title, callback_data="product_buying")
        inline_keyboard.add(button)

    bot.send_message(message.chat.id, "Выберите продукт для покупки:", reply_markup=inline_keyboard)

# Хэндлер для кнопки "Купить"
@bot.message_handler(func=lambda message: message.text == "Купить")
def handle_buy(message):
    get_buying_list(message)

# Хэндлер для callback_data
@bot.callback_query_handler(func=lambda call: call.data == "product_buying")
def send_confirm_message(call):
    bot.answer_callback_query(call.id)  # Убирает вращающийся значок на кнопке
    bot.send_message(call.message.chat.id, "Вы успешно приобрели продукт!")

bot.polling()
