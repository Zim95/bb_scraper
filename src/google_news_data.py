#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: Main Task Runner
Author: NamahRecoSense
"""
# built-in imports
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import json
import time
import uuid
from datetime import datetime, timedelta
from dateutil import parser

# app imports
from driver import firefox_driver_headless


def read_from_file():
    with open('../data/mobile_urls.json', 'r') as f:
        lines = f.readlines()
    return lines


def write_to_file(dictionary):
    with open('../data/sports_news_data.json', 'a') as f:
        f.write(json.dumps(dictionary)+"\n")
    return


def get_category_text(text):
    text = text.lower()
    text = text.replace("'", '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('&', '')
    text = text.replace(',', '')
    text = text.replace(' ', '-')

    return text


ALLOWED_SOURCES = ['Reuters India', 'Reuters']


def get_all_items(url):
    url_list = []
    driver_obj = firefox_driver_headless.SeleniumWebDriver()
    driver = driver_obj.driver
    driver.get(url)

    item_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]"
            )
        )
    )

    item_list = item_div.find_elements_by_xpath(
        ".//div"
    )

    for item in item_list:
        try:
            item_source = item.find_element_by_xpath(
                ".//div/article/div[2]/div/a"
            )
            
            source = item_source.text
            print(source)
            if source in ['Reuters', 'Reuters India', 'Fox Sports', 'FOXSports.com']:
                article_url = item.find_element_by_xpath(
                    ".//div/article/a"
                )
                item_url = article_url.get_attribute('href')
                url_list.append(item_url)
        except Exception as e:
            print('Error: ' + str(e))
            continue

    driver.quit()
    return url_list


def scrape():
    pass


def reuter_image_parser(image_text):
    return 'https:' + image_text.split(
        ":")[1].strip().split(";")[0].split(
            "(")[1].split("\"")[1]


def fox_sport_date_parser(date_text):
    next_date_string = parser.parse(date_text)
    next_date_string + timedelta(days=1)
    next_date_string = datetime.strftime(
        next_date_string,
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return date_text, next_date_string


def reuter_date_parser(date_text):
    month_dictionary = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12,
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
    }

    date_text = date_text.lower()

    y_m_d = date_text.split("/")[0].strip()
    h_m_ext = date_text.split("/")[1].strip()

    y_m_d_list = y_m_d.split(" ")
    month = str(
        month_dictionary[y_m_d_list[0].strip(" ")]
    )
    day = int(y_m_d_list[1].strip(" ").strip(","))
    year = y_m_d_list[2].strip(" ")

    h_m_list = h_m_ext.split(" ")[0].split(":")
    hour = int(h_m_list[0])
    minutes = int(h_m_list[1])
    ext = h_m_ext.split(" ")[1].strip(" ")
    if ext != "AM":
        hour += 12
        if hour >= 24:
            hour = hour - 12
    
    start_date_string = "{}-{}-{}T{}:{}:{}.{}Z".format(
        year,
        month,
        str(day),
        str(hour),
        str(minutes),
        "00",
        "0000"
    )
    end_date_string = "{}-{}-{}T{}:{}:{}.{}Z".format(
        year,
        month,
        str(day + 1),
        str(hour),
        str(minutes),
        "00",
        "0000"
    )
    return start_date_string, end_date_string


def reuters_scraper(url_list, genre='', category=''):
    for url in url_list:
        try:
            driver_obj = firefox_driver_headless.SeleniumWebDriver()
            driver = driver_obj.driver
            driver.get(url)

            title_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[4]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/h1'
                    )
                )
            )
            title = title_tag.text

            description_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                         By.XPATH,
                         '/html/body/div[4]/div/div[1]/div/div/div[2]/div[2]/div[1]/div/div[1]/p[1]'
                    )
                )
            )
            description = description_tag.text

            image_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[4]/div/div[1]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/figure/div[1]/div'
                    )
                )
            )
            image = reuter_image_parser(image_tag.get_attribute('style'))

            date_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[4]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div[2]'
                    )
                )
            )
            start_date_string, end_date_string = reuter_date_parser(date_tag.text)

            provider = "mediasense_news_scraper"
            item_id = uuid.uuid4().hex
            if not provider:
                return {}
            if not item_id:
                return {}

            strfstring = "%Y-%m-%dT%H:%M:%S.%fZ"
            cast = ''
            category = ['sport']
            published_at = start_date_string

            starts_at = start_date_string
            ends_at = end_date_string
            schedule = {
                'ends_at': ends_at,
                'starts_at': starts_at
            }

            release_date = starts_at
            last_modified = datetime.strftime(
                datetime.utcnow(),
                strfstring
            )

            tags = []
            item_type = 'article'

            state = 'active'
            language = 'en'
            genre = genre

            kg_cast = {}
            kg_update = False

            item_dict = {
                "client_id": provider, "item_id": item_id, "cast": cast,
                "category": category, "description": description,
                'recosense_metadata': {
                    'annotation': kg_cast, 'tags': tags},
                "genres": [genre], "image": image, "item_list_type": genre,
                "item_type": item_type, "kg_update": kg_update, "language": language,
                "last_modified": last_modified, "published_date": published_at,
                "released_date": release_date, "schedule": schedule, "state": state,
                "title": title,
            }

            write_to_file(item_dict)

            driver.quit()
        except Exception as e:
            print('Error: ' + str(e))
            continue


def foxnews_scraper(url_list, genre='', category=''):
    for url in url_list:
        try:
            driver_obj = firefox_driver_headless.SeleniumWebDriver()
            driver = driver_obj.driver
            driver.get(url)

            title_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[7]/main/div/div/div[2]/div/div/div/div[1]/div[1]/article/header/h1'
                    )
                )
            )
            title = title_tag.text

            description_string = ''
            for i in range(1, 8):
                try:
                    description_tag = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '/html/body/div[7]/main/div/div/div[2]/div/div/div/div[1]/div[1]/article/div/div[1]/p[{}]'.format(
                                    str(i))
                            )
                        )
                    )
                    description = description_tag.text
                    description_string = description_string + ' ' + description
                    print(description_string)
                except:
                    continue

            image_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[7]/main/div/div/div[2]/div/div/div/div[1]/div[1]/article/header/div[3]/figure/img'
                    )
                )
            )
            image = image_tag.get_attribute('src')

            date_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[7]/main/div/div/div[2]/div/div/div/div[1]/div[1]/article/header/div[2]/ul/li[1]/time'
                    )
                )
            )
            starts_at, ends_at = fox_sport_date_parser(date_tag.get_attribute('datetime'))

            provider = "mediasense_news_scraper"
            item_id = uuid.uuid4().hex

            cast = ''
            category = ['sport']
            published_at = starts_at

            schedule = {
                'ends_at': ends_at,
                'starts_at': starts_at
            }

            release_date = starts_at
            last_modified = datetime.strftime(
                datetime.utcnow(),
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            tags = []
            item_type = 'article'

            state = 'active'
            language = 'en'

            kg_cast = {}
            kg_update = False

            item_dict = {
                "client_id": provider, "item_id": item_id, "cast": cast,
                "category": category, "description": description_string,
                'recosense_metadata': {
                    'annotation': kg_cast, 'tags': tags},
                "genres": [genre], "image": image, "item_list_type": genre,
                "item_type": item_type, "kg_update": kg_update, "language": language,
                "last_modified": last_modified, "published_date": published_at,
                "released_date": release_date, "schedule": schedule, "state": state,
                "title": title,
            }

            write_to_file(item_dict)
            print('success')

            driver.quit()
        except Exception as e:
            driver.quit()
            print('Error: ' + str(e))
            continue


def foxsports_dot_com_scraper(genre='football'):
    with open('emergency_sport_data.txt', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        try:
            strfstring = "%Y:%m:%dT%H:%M:%S.%fZ"

            title = line.split("::")[0]

            description_string = line.split("::")[1]
            image = line.split("::")[2]

            starts_at = datetime.strftime(datetime.utcnow(), strfstring)
            ends_at = datetime.strftime(
                datetime.utcnow() + timedelta(weeks=4),
                strfstring
            )

            provider = "mediasense_news_scraper"
            item_id = uuid.uuid4().hex

            cast = ''
            category = ['sport']
            published_at = starts_at

            schedule = {
                'ends_at': ends_at,
                'starts_at': starts_at
            }

            release_date = starts_at
            last_modified = datetime.strftime(
                datetime.utcnow(),
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            tags = []
            item_type = 'article'

            state = 'active'
            language = 'en'

            kg_cast = {}
            kg_update = False

            item_dict = {
                "client_id": provider, "item_id": item_id, "cast": cast,
                "category": category, "description": description_string,
                'recosense_metadata': {
                    'annotation': kg_cast, 'tags': tags},
                "genres": [genre], "image": image, "item_list_type": genre,
                "item_type": item_type, "kg_update": kg_update, "language": language,
                "last_modified": last_modified, "published_date": published_at,
                "released_date": release_date, "schedule": schedule, "state": state,
                "title": title,
            }

            write_to_file(item_dict)
            print('success')

        except Exception as e:
            print('Error: ' + str(e))
            continue


def main():
    # reuters_url_list = [
    #     {
    #         'url': 'https://news.google.com/search?q=reuters%20sports%20cricket&hl=en-IN&gl=IN&ceid=IN%3Aen',
    #         'genre': 'cricket'
    #     },
    #     {
    #         'url': 'https://news.google.com/search?q=reuters%20sport%20football&hl=en-IN&gl=IN&ceid=IN%3Aen',
    #         'genre': 'football'
    #     },
    #     {
    #         'url': 'https://news.google.com/search?q=reuters%20sport%20tennis&hl=en-IN&gl=IN&ceid=IN%3Aen',
    #         'genre': 'tennis'
    #     }
    # ]

    # for url_list in reuters_url_list:
    #     genre = url_list['genre']
    #     reuters_url_list = get_all_items(url_list['url'])
    #     reuters_scraper(reuters_url_list, genre=genre)

    foxnews_url_list = [
        # {
        #     'url': 'https://news.google.com/search?q=fox%20sports%20cricket&hl=en-IN&gl=IN&ceid=IN%3Aen',
        #     'genre': 'cricket'
        # },
        {
            'url': 'https://news.google.com/search?q=fox%20sports%20soccer&hl=en-IN&gl=IN&ceid=IN%3Aen',
            'genre': 'football' 
        }
        # {
        #     'url': 'https://news.google.com/search?q=fox%20sports%20tennis&hl=en-IN&gl=IN&ceid=IN%3Aen',
        #     'genre': 'tennis'
        # }
    ]

    # for url_list in foxnews_url_list:
    #     genre = url_list['genre']
    #     foxnews_url_list = get_all_items(url_list['url'])
    foxsports_dot_com_scraper()
    # foxnews_url_list = get_all_items(foxnews_url)

    # print('Reuters...................')
    # print(reuters_url_list)
    # print('Fox news..................')
    # print(foxnews_url_list)

if __name__ == "__main__":
    main()
