import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
import sqlite3
import datetime
import re

def datanow(data):
    if datacheck(data) == True:
        nstr = data
        nstr = nstr[3] + nstr[4] + '-' + nstr[0] + nstr[1]
    if (data == 'now'):
        nstr = datetime.datetime.now().strftime("%m-%d")
    if (data == 'tomorrow'):
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        nstr = now.strftime("%m-%d")

    return nstr
now = datetime.datetime.now() + datetime.timedelta(days=1)
now = now.strftime("%m-%d")
sqllist = ['Дата: ', 'Время: ', 'Название: ', 'Адрес: ']

def sql_man(data):
    con = sqlite3.connect(r'res/tangodatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT " + '*' + " FROM lessons where date = '" + datanow(data) + "' order by date desc;")
    sqll = cur.fetchall()
    con.cursor().close()
    con.close()

    return sqll

def parslist(sqlist, ind):
    sqlstr = ''
    #for kind in range(len(sqlist[0][0])):
     #   sqlstr = sqlstr + '\n'
    for kpar in range(len(sqlist[ind])):
        sqlstr = sqlstr + sqllist[kpar] + sqlist[ind][kpar] + '\n'
    return sqlstr

def datacheck(data):
    match = re.search(r'\d{2}.\d{2}', data)
    #date = datetime.strptime(match.group(), '%m-%d').date()
    #print(date)
    if (match != None):
        result = True
    else:
        result = False
    return result

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
flaglist = [0,0,0,0,0,0]

@dp.message_handler(commands=['today'])
async def send_welcome(message: types.Message):
    srts = sql_man('now')
    for i in range(len(srts[0][0])):
        await message.reply(parslist(srts, i))

@dp.message_handler(commands=['tomorrow'])
async def send_welcome(message: types.Message):
    srts = sql_man('tomorrow')
    for i in range(len(srts[0][0])):
        await message.reply(parslist(srts, i))

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
    await message.reply("У меня лапки..")

@dp.message_handler(commands=['data'])
async def send_welcome(message: types.Message):
    await message.answer("Укажите дату в формате: 'dd.mm'")
    flaglist[0] = 0
    if (datacheck(str(message.text)) == True):
        srts = sql_man(message.text)
        for i in range(len(srts[0][0])):
            await message.answer(parslist(srts, i))

@dp.message_handler(commands=['schedule'])
async def send_welcome(message: types.Message):
    await message.answer("Расписание пока не готово")

@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Напишу дату":
        await message.answer("Укажите дату в формате: 'dd.mm'")
        flaglist[0] = 0
    if (datacheck(str(message.text)) == True):
        srts = sql_man(message.text)
        for i in range(len(srts[0][0])):
            await message.answer(parslist(srts, i))
    else:
        if (flaglist[0] == 1):
            await message.answer("Что-то пошло не так")
        flaglist[0] = 1
    if message.text == "Завтра":
        srts = sql_man('tomorrow')
        for i in range(len(srts[0][0])):
            await message.answer(parslist(srts, i))
    if message.text == "Сегодня":
        srts=sql_man('now')
        for i in range(len(srts[0][0])):
            await message.answer(parslist(srts, i))
    if message.text == "Что есть на неделе?":
        await message.answer("Что-то пошло не так")
    if message.text == "пидр":
        await message.answer("сам такой")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)