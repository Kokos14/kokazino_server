import asyncio
import logging
import sys

import os
import psycopg2
import ssl

import asyncio
import websockets

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from aiogram.types.web_app_info import WebAppInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


import requests

def get_ip_address():
    try:
        response = requests.get("http://httpbin.org/ip")
        if response.status_code == 200:
            ip_address = response.json()["origin"]
            return ip_address
        else:
            print("Ошибка при получении IP-адреса:", response.status_code)
            return None
    except Exception as e:
        print("Ошибка при запросе к httpbin.org:", e)
        return None

# Получаем и выводим IP-адрес
print("IP-адрес вашего компьютера:", get_ip_address())

DATABASE_URL = "postgresql://kokoz:jYL0n5iYiuHGR4Vl4TUe9g@tg-test-9200.7tc.aws-eu-central-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with conn.cursor() as cur:
    cur.execute("SELECT * FROM tg")
    res = cur.fetchall()
    conn.commit()
    print(res)


async def hello(websocket, path):
    # Принимаем подключение
    print("Подключение установлено")

    try:
        # Получаем сообщения от клиента
        async for message in websocket:
            print(f"Получено сообщение от клиента: {message}")

            # Отправляем ответ клиенту
            await websocket.send(f"Вы сказали: {message}")
            print(f"Отправлено сообщение клиенту: {message}")

    except websockets.exceptions.ConnectionClosedOK:
        print("Соединение с клиентом закрыто")


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
start_server = websockets.serve(hello, "kokazinoserver-production.up.railway.app", 7865) #ssl=ssl_context

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

print("SERVER WORK")


TOKEN = "6809197177:AAH0EAFMSxe_Im9d_BtA4Wg3IzFFdr-F6Dk"

print(str(TOKEN))

dp = Dispatcher()

@dp.message(Command(("start"), prefix="!/"))
async def command_start_handler(message: types.Message):

    tg_channel_btn = InlineKeyboardButton(text='Открыть вёб', web_app=WebAppInfo(url='https://kokos14.github.io/kok1/'))

    row = [tg_channel_btn]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await message.answer('Darova', reply_markup=markup)

#@dp.message_handler(content_types=['web_app_data'])
#async def web_app(message: types.Message):
#    await message.answer(message.web_app_data)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
