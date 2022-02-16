# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 22:33:06 2022

@author: magika
"""

import time
import sqlite3
from tango_map import opener as _map
from tango_city import parser as city
import asyncio
import nest_asyncio
import aiosqlite3
nest_asyncio.apply()
# from Tango_city_2 import main as city


async def construct_data(loop):
    con = await aiosqlite3.connect("tangodatabase.db", loop=loop)
    cur = await con.cursor()
    await cur.execute("""DROP TABLE IF EXISTS lessons""")
    await con.commit()
    await cur.execute("""CREATE TABLE IF NOT EXISTS lessons(
        date TEXT,
        time TEXT,
        job TEXT,
        adres TEXT,
        dj TEXT,
        link TEXT
        )""")
    await con.commit()
    for funk in asyncio.as_completed([_map(), city()]):
        i = await funk
        for tuple1 in i:
            await cur.executemany("""INSERT INTO lessons(date,time,job,adres,dj,link) VALUES (?,?,?,?,?,?)""", tuple1)
            await con.commit()
    # time.sleep(10)1
    await cur.execute("""SELECT
                   date, job,adres, COUNT(*)
                   FROM
                   lessons
                   GROUP BY
                   date, job, adres
                   HAVING 
                   COUNT(*) > 1""")
    await con.commit()
    await cur.execute("""SELECT
                   date, dj, COUNT(*)
                   FROM
                   lessons
                   GROUP BY
                   date, dj
                   HAVING 
                   COUNT(*) > 1""")
    await con.commit()   


def main():
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(construct_data(event_loop))
    # return construct_data()


if __name__ == "__main__":
    main()
