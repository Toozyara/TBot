"""
@author: Toozyara
"""

import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import sys
import time
import asyncio
import conf
import sqlite3
import datetime
import re

sys.path.append(os.path.abspath("./res/"))
from res.switch import main
#from res import untitled12

#import res.untitled12
#import res.Tango_map as Tango_map
#import res


#from res.untitled12 import construct_data
""" переделать для лини, не работает без конды
sys.path.append(os.path.abspath("./res/"))
from res.untitled12 import construct_data

start = time.time()
"""

def datanow(data):
    if datacheck(data):
        nstr = data
        nstr = nstr[3] + nstr[4] + '.' + nstr[0] + nstr[1]
    elif data == 'now':
        nstr = datetime.datetime.now().strftime("%m.%d")
    elif data == 'tomorrow':
        o_now = datetime.datetime.now() + datetime.timedelta(days=1)
        nstr = o_now.strftime("%m.%d")
    elif data == "*":
        pika = " SELECT * FROM lessons "
        return pika
    pika = f"SELECT * FROM lessons where date = '{nstr}' order by date desc;"
    return pika

    """
#o_now = datetime.datetime.now() + datetime.timedelta(days=1)
#now = o_now.strftime("%m-%d")
"""
sqllist = [
    'Дата: ', 'Время: ', 'Название: ', 'Адрес: ', 'DJ: ', 'Ссылка: '
    ]

def sql_man(data):
    con = sqlite3.connect(r'tangodatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(datanow(data))
    sqll = cur.fetchall()
    con.cursor().close()
    con.close()

    return sqll

def parslist(sqlist, ind):
    sqlstr = ''
    for kpar in range(len(sqlist[ind])):
        sqlstr = sqlstr + sqllist[kpar] + sqlist[ind][kpar] + '\n'
    return sqlstr
def datacheck(data):
    match = re.search(r'\d{2}.\d{2}', data)
    """
    #date = datetime.strptime(match.group(), '%m-%d').date()
    #print(date)
    """
    if match != None:
        result = True
    else:
        result = False
    return result

bot_token = conf.TOKEN_A
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

"""updata = asyncio.ensure_future(update_data())

update_loop = asyncio.get_event_loop()
asyncio.set_event_loop(update_loop)
update_loop.run_until_complete(asyncio.gather(updata))
update_loop.close()"""

flaglist = [0]

async def print_scheduler(message: types.Message, when=''):
    srts = sql_man(when)
    for j in range(len(srts)):
        await asyncio.sleep(0.05)
        await message.reply(parslist(srts, j))

async def print_schedule(message: types.Message, when=''):
    srts = sql_man(when)
    for i in range(len(srts)):
        await asyncio.sleep(0.05)
        await message.answer(parslist(srts, i))

@dp.message_handler(commands=['update'])
async def up(message: types.Message):
    main()
    await message.reply('Ok!')

@dp.message_handler(commands=['today'])
async def beka(message: types.Message):
    await print_scheduler(message, 'now')

@dp.message_handler(commands=['tomorrow'])
async def send_welcome(message: types.Message):
    await print_scheduler(message, 'tomorrow')

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_1 = ["Сегодня", "Завтра"]
    buttons_2 = ["Напишу дату", "Что есть на неделе?"]
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
    if datacheck(str(message.text)):
        await print_scheduler(message, message.text)

@dp.message_handler(commands=['schedule'])
async def send_welcome(message: types.Message):
    await message.answer("Расписание пока не готово")

@dp.message_handler()
async def echo(message: types.Message):
    try:
        flaglist[0] = 0
        if message.text == "Напишу дату":
            await message.answer("Укажите дату в формате: 'dd.mm'")
        elif datacheck(message.text):
            await print_schedule(message, message.text)
        elif message.text == "Завтра":
            await print_schedule(message, 'tomorrow')
        elif message.text == "Сегодня":
            await print_schedule(message, 'now')
        elif message.text == "Что есть на неделе?":
            await print_scheduler(message, '*')
        elif message.text == "нет спасибо":
            await message.answer("я не голодный")
        else:
            if flaglist[0] == 1:
                await message.answer("Что-то пошло не так")
    except TypeError:
        flaglist[0] = 1

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
