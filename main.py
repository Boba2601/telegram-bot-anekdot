import config
import requests
import random
from bs4 import BeautifulSoup as b
import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types

#log
logging.basicConfig(level=logging.INFO)

#init
bot = Bot(token=config.token, parse_mode='html')
dp = Dispatcher(bot)
URL = 'https://anekdotov.net/anekdot/'

def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='anekdot')
    return [c.text for c in anekdots]

list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)

@dp.message_handler(commands=['start'])
async def get_message(message: types.Message):
    text = f'Добро пожаловать <b>{message.from_user.full_name}</b>, хочешь анекдот? Введи цифру c 1-9.'
    await bot.send_message(message.chat.id, text=text)

@dp.message_handler(content_types=['text'])
async def jokes(message: types.Message):
    if message.text.lower() in '123456789':
        await bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        await bot.send_message(message.chat.id, 'Я тебя не понял введи цифру')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
