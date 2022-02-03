import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
import sqlite3
import datetime

def datanow(dataday):
    if data
    now = datetime.datetime.now()
    nstr= '0' + str(100 * now.month + now.day)
    if (len(nstr)==4):
        nstr = nstr[0] + nstr[1] + '-' + nstr[2] + nstr[3]
    else:
        nstr = nstr[1] + nstr[2] + '-' + nstr[3] + nstr[4]
    return (nstr)

#print(datanow())

def sql_connection():
    con = sqlite3.connect(r'res/tangodatabase.db')
    return con

sqllist = ['Дата: ', 'Время: ', 'Название: ', 'Адрес: ']

def sql_table(select):
    sql_connection().row_factory = sqlite3.Row
    cur = sql_connection().cursor()
    cur.execute(select)
    return(cur.fetchall())


def locbase():
    for sq in sqllist:
        sqlselect = "SELECT " + '*' + " FROM lessons where date = '" + datanow() + "' order by date desc;"
        #print(sql_table(sqlselect))
        sqll = sql_table(sqlselect)
        sql_connection().cursor().close()
        sql_connection().close()
    return sqll

def parsql(sqlist, ind):
    #print(len(sqlist[0]))
   # print(len(sqlist[0][0]))
    sqlstr = ''
    #for kind in range(len(sqlist[0][0])):
     #   sqlstr = sqlstr + '\n'
    for kpar in range(len(sqlist[ind])):
        sqlstr = sqlstr + sqllist[kpar] + sqlist[ind][kpar] + '\n'
    return sqlstr

#locbase()

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
        srts=locbase()
        for i in range(len(srts[0][0])):
            await message.answer(parsql(locbase(), i))
    if message.text == "Что есть на неделе?":
        await message.answer("Расписание готовится")
    if message.text == "пидр":
        await message.answer("сам такой")
    #else:
      #  await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)