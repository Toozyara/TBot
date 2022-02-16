# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 21:57:22 2022

@author: magika
"""

from bs4 import BeautifulSoup as bs
import datetime
import asyncio
import aiohttp


# async def opener():
    

async def parser():
    list_of_month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                     'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}
    now = datetime.datetime.now().strftime("%m-%d")

    async def date_trans(cell):

        data = cell.find(class_='data').text.strip().split()
        day = '0'*(2-len(data[0].strip()))+data[0].strip()
        month = list_of_month[data[1].strip()]
        date = f'{month}-{day}'
        if date < now:
            # print(now,date)
            return '' 
        return f'{month}.{day}'

    async def practics(cell):
        acum = []
        for i in cell.find_all('td')[2].find_all(style='text-align: left;'):
            if i.find('del'):
                acum += ['']
                continue
            acum += [i.text.strip().replace('\n', ' ').replace('\xa0', ' ')]
        return acum

    async def urls(cell):
        acum = []
        for i in cell.find_all('td')[6].find_all('div'):
            try:
                piece = i.find('a').get('href')
            except AttributeError:
                piece = ''
            acum += [piece]
        return acum

    url = r'http://www.tangocity.ru/afisha/milongi'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as reap:
            reap_text = await reap.text()
            soup = bs(reap_text, 'lxml')
            data = []
            for cell in soup.find_all(style="background-color: #ebebeb;"):
                # print(cell.text)
                date = await date_trans(cell)
                # print(date)
                if not date:
                    continue
                dj = [i.text.replace('dj', '').strip()
                      or '' for i in cell.find_all('td')[4].find_all('div')]
                lessons = await practics(cell)
                adres = [i.find_parent().text.replace('\xa0', ' ').strip()
                         for i in cell.select('[href]') if i.text]
                time = [i.text.replace('\n', ' ').replace('\xa0', ' ').strip()
                        for i in cell.find_all('td')[-2].find_all(style='text-align: left;')]
                dates = (len(time))*[date]
                # print(dates)
                url = await urls(cell)
                out = tuple([(i0, i1, i2, i3, i4, i5) for i0, i1, i2, i3, i4, i5 in zip(
                    dates, time, lessons, adres, dj, url) if i2 !=''])
                data.append(out)
            return data


def main():
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(parser())


if __name__ == '__main__':
    for i in main():
        print(i)
    # main()
