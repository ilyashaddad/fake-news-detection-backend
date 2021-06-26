from __future__ import absolute_import, unicode_literals

import requests
from time import sleep
import csv
import os
from bs4 import BeautifulSoup

from celery import shared_task
from .models import News_s

# from fake_useragent import UserAgent


@shared_task
def news_task():
    print("Collecting news article..")
    urls = [
       # "https://www.aljazeera.net/news/politics",
        #"https://www.aljazeera.net/news/ebusiness",
        #"https://www.aljazeera.net/news/cultureandart",
        #'https://www.aljazeera.net/sport',
        #"https://www.aljazeera.net/news/arts"
        #'ljazeera.net/news/scienceandtechnology',
       # "https://www.aljazeera.net/turath",
       # "https://www.aljazeera.net/news/science",
    ]
    data_url = [
        "https://github.com/latynt/ans/blob/master/data/claim/train.csv",
    ]
    # user_agent = UserAgent()
    for u in data_url:
        r = requests.get(u)
        print(u)
        htmlcontent = r.content
        soup = BeautifulSoup(htmlcontent, "html.parser")
        rows = soup.find_all("tr")[2:]
        for row in rows:
            tds = row.find_all("td")
            News_s.objects.create(
                title=tds[1].text,
                resume="resume",
                date="date",
                image="",
                thematic="thematic",
                description="description",
                fake_flag=tds[2].text,
            )

    for url in urls:
        print(url)
        print(url)
        r = requests.get(url)
        htmlcontent = r.content
        # print(htmlcontent)

        soup = BeautifulSoup(htmlcontent, "html.parser")
        # print(soup.prettify)

        rows = soup.find_all("article")

        for row in rows:
            thematic = soup.find("div", class_="section-header__title").get_text()
            title = row.find("span").get_text()
            resume = row.find("p").get_text()
            date = row.find(
                "div", class_="date-simple css-1mfvvdi-DateSimple"
            ).get_text()
            image = row.find("img").get("src")
            link = row.find("a").get("href")
            link = "https://www.aljazeera.net" + link
            description = details(link)

            News_s.objects.create(
                title=title,
                resume=resume,
                date=date,
                image="https://www.aljazeera.net/" + image,
                thematic=thematic,
                description=description,
                fake_flag=1,
            )

            sleep(5)


def details(link):
    d = requests.get(link)
    htmlcontent = d.content
    soupd = BeautifulSoup(htmlcontent, "html.parser")
    rows = soupd.find("div", class_="wysiwyg wysiwyg--all-content css-1mw1dwe").findAll(
        "p"
    )
    description = " "
    for row in rows:
        description += " . " + "".join(row.findAll(text=True))
    return description


news_task()
