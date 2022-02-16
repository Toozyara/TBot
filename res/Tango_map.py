"""
Created on Sat Jan 22 22:33:06 2022

@author: magika
"""
from bs4 import BeautifulSoup as bs
import requests as req
import datetime
import re


def parcer():
    url = r"http://tango-map.ru/ru/"
    reap = req.get(url)
    now = datetime.datetime.now().strftime("%m-%d")

    def adress(work_material):
        return work_material.h3.text.strip().replace('Москва', '').strip(' ,.\n')

    # def phone():  # Функция поиска телефона в текстом html
        # return re.findall(r'(?:|\+7|\+8|7|8)(?: |)(?:\(\d{3}\)|\d{3})(?:|-| )(?:\d{3})(?:|-| )(?:\d{2})(?:|[-]| )(?:\d{2})', work_material.text)

    def time_(work_material):  # Функция поиска времени
        time_place = work_material.find_all('h3')[1]
        return time_place.find(text=re.compile(r'^(?:(?!руб).)*?$', flags=re.MULTILINE))

    def dj(work_material):
        try:
            return re.search(r'(?:DJ|dj)(?:.)*', work_material.text)[0]
        except TypeError:
            return None
    table = bs(reap.text, 'lxml')

    for teg in table.findAll(class_='djev_item_content'):
        date_in_url = teg.find('a')['href'].strip()
        date = re.search(r"\d{4}-\d{2}-\d{2}", date_in_url)[0][5:]
        if now > date:
            continue
        practic = teg.find('a').text.strip()[:-5]
        if 'милонга' not in practic.lower() or 'практика' in practic.lower():
            continue
        url_for_lesson = url[:-4]+date_in_url
        reap_for_link = req.get(url_for_lesson)
        # Здесь создается все необходимое для перехода по ссылкам
        table_for_lesson = bs(reap_for_link.text, "html.parser")
        work_material = table_for_lesson.find(class_="djev_fulltext")
        yield ((date, time_(work_material), practic, adress(work_material), dj(work_material), url_for_lesson),)


def main():
    return parcer()


if __name__ == "__main__":
    for i in main():
        print(i)