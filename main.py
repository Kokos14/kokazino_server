import asyncio
import logging
import sys

import os
import psycopg2

import asyncio
import websockets

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from aiogram.types.web_app_info import WebAppInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DATABASE_URL = "postgresql://kokoz:jYL0n5iYiuHGR4Vl4TUe9g@tg-test-9200.7tc.aws-eu-central-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with conn.cursor() as cur:
    cur.execute("SELECT * FROM tg")
    res = cur.fetchall()
    conn.commit()
    print(res)

#os.system('pause')

# Функция, которая будет вызываться при подключении клиента
async def hello(websocket, path):
    # Отправляем сообщение при подключении
    await websocket.send("Добро пожаловать! Вы подключены к WebSocket серверу.")

    try:
        while True:
            # Получаем сообщение от клиента
            message = await websocket.recv()
            print(f"Получено сообщение от клиента: {message}")

            # Отправляем обратно полученное сообщение
            await websocket.send(f"Вы сказали: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Соединение с клиентом закрыто.")

print("SERVER START")
# Запуск WebSocket сервера на localhost:8765
start_server = websockets.serve(hello, "kok1.railway.internal", 8765)

print("SERVER CONNECT")

# Запускаем сервер в асинхронном режиме
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
