# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 21:57:22 2022

@author: magika
"""

from bs4 import BeautifulSoup as bs
import requests as req
import re
import datetime
import pandas as pd


def parser():
    list_of_month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                     'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}
    now = datetime.datetime.now().strftime("%m-%d")

    def date_trans(cell):

        data = cell.find(class_='data').text.strip().split()
        day = '0'*(2-len(data[0].strip()))+data[0].strip()
        month = list_of_month[data[1].strip()]
        return f'{month}-{day}'

    url = r'http://www.tangocity.ru/afisha/milongi'
    reap = req.get(url)
    soup = bs(reap.text, 'lxml')
    dates = []
    lessons = []
    adres_data = []
    time_data = []
    url_data = []
    for cell in soup.find_all(style="background-color: #ebebeb;"):
        date = date_trans(cell)
        if date < now:
            continue
        lessons += [i.text.strip().replace('\n', ' ').replace('\xa0', ' ')
                    for i in cell.find_all('td')[2].find_all(style='text-align: left;')]
        adres_data += [i.find_parent().text.strip().replace('\xa0', ' ') for i in cell.select('[href]') if i.text]
        time_data += [i.text.strip() for i in cell.find_all('td')[-2].find_all(style='text-align: left;')]
        dates += (len(time_data)-len(dates))*[date]
        url_data += [i['href'] for i in cell.find_all('td')[3].select('[href]')]
    data_colecter = pd.DataFrame({"Дата": dates, "Время": time_data, "Вид_деятельности": lessons, "Адрес": adres_data})
    # print(data_colecter)
    return data_colecter


def main():
    return parser()


if __name__ == '__main__':
    print(main())
