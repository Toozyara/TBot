import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
"""
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!")
"""

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_1 = ["Сегодня", "Завтра"]
    buttons_2 = ["Напишу дату","Что есть на неделе?"]
    keyboard.add(*buttons_1)
    keyboard.add(*buttons_2)
    await message.answer("Когда пойдём на милонгу?", reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Чем я могу помочь?")

@dp.message_handler(commands=['schedule'])
async def send_welcome(message: types.Message):
    await message.answer("Расписание пока не готово")

@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Напишу дату":
        await message.answer("В ожидании")
    if message.text == "11.07":
        await message.answer("Что-то пошло не так")
    if message.text == "Завтра":
        await message.answer("Что-то пошло не так")
    if message.text == "Сегодня":
        await message.answer("Заполняем расписание")
    if message.text == "Что есть на неделе?":
        await message.answer("Расписание готовится")
    if message.text == "пидр":
        await message.answer("сам такой")
    #else:
      #  await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)