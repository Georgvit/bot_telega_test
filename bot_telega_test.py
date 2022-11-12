from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram import types
import wikipedia

wikipedia.set_lang("ru")

import re
import random
import asyncio
import logging
import os

# Добавляем логирование
logging.basicConfig \
    (level=logging.DEBUG,
     filename='my_program_log.log',
     format='%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
     datefmt='%H:%M:%S')

# Подключаем токен бота
bot = Bot(token=os.getenv('TOKEN'))
# Диспетчер
dp = Dispatcher(bot)

# Открываем файл с анекдотами
f = open('funny_jokes.txt', 'r', encoding='UTF-8')
jokes = f.read().split('???')
f.close()
length_list_jokes = len(jokes)


# Функция запроса данных в вики
def get_ru_wiki(user_text):
    try:
        # Загружаем страницу вики
        page_info = wikipedia.page(user_text)
        # Получаем первую тысячу символов
        wikitext = page_info.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем все после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей п
                # еременной и возвращаем утерянные при разделении строк точки на место
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


# Стартовое меню
def start_menu():
    builder = types.InlineKeyboardMarkup(row_width=1)
    button = [types.InlineKeyboardButton(text='Веселые анекдоты 🤣🤣🤣', callback_data='jokes'),
              types.InlineKeyboardButton(text='Умные мысли 🎓🎓🎓', callback_data='smart')]
    builder.add(*button)
    return builder


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def reply_buider(message: types.Message):
    await message.answer('Приветствую 👋 \nЧем тебя развлечь?😎', reply_markup=start_menu())


# Хендлер на команду /jokes
@dp.callback_query_handler(text='jokes')
async def call_hand_jokes(call: types.CallbackQuery):
    ran = random.randint(1, length_list_jokes - 1)
    await call.message.answer(jokes[ran])
    separator = '🔥'
    await call.message.answer(separator * 12)
    await call.message.answer('Тебе понравилось? 😉 \nЧем еще тебя развлечь? 😎', reply_markup=start_menu())


# Хендлер на команду /smart
@dp.callback_query_handler(text='smart')
async def call_hand_smart(call: types.CallbackQuery):
    await call.message.answer('Введите слово и я найду его в Wikipedia')


# Пользовательский ввод для поиска в википедии
@dp.message_handler()
async def answer_wiki(message: types.Message):
    await message.answer(get_ru_wiki(message.text))
    separator = '🔥'
    await message.answer(separator * 12)
    await message.answer('Тебе понравилось? 😉 \nЧем еще тебя развлечь? 😎', reply_markup=start_menu())


# Запуск опроса новых апдейтов
executor.start_polling(dp, skip_updates=True)
