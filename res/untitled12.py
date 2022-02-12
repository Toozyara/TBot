# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 22:33:06 2022

@author: magika
"""

import sqlite3
import pandas as pd
from Tango_map import main as _map
from Tango_city import main as city


def construct_data():
    con = sqlite3.connect("tangodatabase.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS lessons(
        date Date,
        time TEXT,
        job TEXT,
        adres TEXT,
        dj TEXT,
        link TEXT
        )""")
    con.commit()

    data_map = _map()
    data_city = city()
    data_unit = pd.concat([data_map, data_city], ignore_index=True)
    # data_for_com = pd.DataFrame({"Дата": [], "Время": [], "Вид_деятельности": [],
                                 # "Адрес": [], 'Диджей': [], "Ссылка": []})
    # for i in cursor.execute("""SELECT * FROM lessons"""):
    #     data_for_com = data_for_com.append({"Дата": i[0], "Время": i[1], "Вид_деятельности": i[2],
    #                                         "Адрес": i[3], 'Диджей': i[4], 'Ссылка': i[5]}, ignore_index=True)
    data_unit = data_unit.sort_values(by="Дата")
    # if not data_unit.equals(data_for_com):
    cursor.execute("""DROP TABLE lessons""")
    con.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS lessons(
        date Date,
        time TEXT,
        job TEXT,
        adres TEXT,
        dj TEXT,
        link TEXT
        )""")
    con.commit()
    for i in data_unit.iloc:
        cursor.execute("""INSERT INTO lessons VALUES (?,?,?,?,?,?)""",
                       (i[0], i[1], i[2], i[3], i[4], i[5]))
        con.commit()
    cursor.execute("""SELECT
                   date, job,adres, COUNT(*)
                   FROM
                   lessons
                   GROUP BY
                   date, job, adres
                   HAVING 
                   COUNT(*) > 1""")
    con.commit()

if __name__ == "__main__":
    construct_data()
