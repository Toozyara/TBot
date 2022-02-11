"""
Created on Sat Jan 22 22:33:06 2022

@author: magika
"""
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import datetime
import re


def parcer():
    url = r"http://tango-map.ru/ru/"
    reap = req.get(url)
    now = datetime.datetime.now().strftime("%m-%d")
    def adress():
        return work_material.h3.text.strip().replace('Москва', '').strip(' ,.\n')

    # def phone():  # Функция поиска телефона в текстом html
        # return re.findall(r'(?:|\+7|\+8|7|8)(?: |)(?:\(\d{3}\)|\d{3})(?:|-| )(?:\d{3})(?:|-| )(?:\d{2})(?:|[-]| )(?:\d{2})', work_material.text)

    def time_(work_material):  # Функция поиска времени
        time_place = work_material.find_all('h3')[1]
        # print(time_place.text)
        return time_place.find(text=re.compile(r'^(?:(?!руб).)*?$', flags=re.MULTILINE))
    table = bs(reap.text, "html.parser")
     #list_table = self.table.findAll(class_='djev_items djev_clearfix')
     #print(table)s
    list_of_time = []
    list_of_adress = []
    list_of_dates = []
    list_of_url = []
    list_of_practic = []
    for teg in table.findAll(class_='djev_item_content'):
        # print(teg)
        # print(1)
        date_in_url = teg.find('a')['href'].strip()
        date = re.search(r"\d{4}-\d{2}-\d{2}", date_in_url)[0][5:]
        #print(date)
        if now > date:
            continue
        practic = teg.find('a').text.strip()[:-5]
        if ('милонга' not in practic.lower()) or ('практика' in practic.lower()):
            continue
        #print(practic.lower())
        url_for_lesson = url[:-4]+date_in_url
        reap_for_link = req.get(url_for_lesson)
        # Здесь создается все необходимое для перехода по ссылкам
        table_for_lesson = bs(reap_for_link.text, "html.parser")
        work_material = table_for_lesson.find(class_="djev_fulltext")
        #

        list_of_practic.append(practic)
        les_adress = adress()
        # tel = phone() or ["Телефон не указан"] # Может нужно может нет

        time = time_(work_material) or ["Время не указано"]
        # print(time)
        list_of_url.append(url_for_lesson)
        list_of_dates.append(date)
        list_of_adress.append(les_adress)
        list_of_time.append(time)
        # print(list_of_time)
    data =  pd.DataFrame(
        {"Дата": list_of_dates, "Время": list_of_time, "Вид_деятельности": list_of_practic, "Адрес": list_of_adress})
    return data

def main():
    return parcer()


if __name__ == "__main__":
    print(main())
    # A = Tango()
    # A._page()
    # for i in A.data.iloc:
    # print(i)
