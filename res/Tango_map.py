"""
Created on Sat Jan 22 22:33:06 2022

@author: magika
"""
from bs4 import BeautifulSoup as bs
import datetime
import re
import asyncio
import aiohttp
import nest_asyncio
nest_asyncio.apply()


async def opener():
    url = r"http://tango-map.ru/ru/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as reap:
            now = datetime.datetime.now().strftime("%m-%d")
            reap_text = await reap.text()
            table = bs(reap_text, 'lxml')
            data = []
            tasks = [parser(teg, now, url, session)
                     for teg in table.findAll(class_='djev_item_content')]

            for i in asyncio.as_completed(tasks):
                appended = await i
                if appended:
                    data.append(appended)
            return data


async def parser(teg, now, url, session):
    async def adress(work_material):
        return work_material.h3.text.strip().replace('Москва', '').replace('\xa0', '').strip(' ,.\n')

    async def time_(work_material):  # Функция поиска времени
        time_place = work_material.find_all('h3')[1]
        return time_place.find(text=re.compile(r'^(?:(?!руб).)*?$', flags=re.MULTILINE))

    async def dj(work_material):
        try:
            return re.search(r'(?<=DJ|dj)(?:.)*', work_material.text)[0].replace('\xa0', ' ').strip()
        except TypeError:
            return ''

    async def fb_url(work_material):
        return work_material.find(href=True, string=re.compile(r"https:"))['href']

    async def date_converter(date):
        return date.replace('-', '.')
    date_in_url = teg.find('a')['href'].strip()
    date = await date_converter(re.search(r"\d{4}-\d{2}-\d{2}", date_in_url)[0][5:])
    if now > date:
        return ''

    practic = teg.find('a').text.strip()[:-5]
    if 'милонга' not in practic.lower() or 'практика' in practic.lower():
        return ''
    url_for_lesson = url[:-4]+date_in_url
    # print(url_for_lesson)
    async with session.get(url_for_lesson) as reap:
        reap_text = await reap.text()
        # Здесь создается все необходимое для перехода по ссылкам
        table_for_lesson = bs(reap_text, "lxml")
        work_material = table_for_lesson.find(class_="djev_fulltext")
        return ((date, await time_(work_material), practic, await adress(work_material),
                 await dj(work_material), await fb_url(work_material)),)


def main():
    nest_asyncio.apply()
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(opener())


if __name__ == "__main__":
    for i in main():
        print(i)
    # main()
