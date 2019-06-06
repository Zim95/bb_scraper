#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: ErosNow Scraper
Author: NamahRecoSense
"""
# built-in imports

import json
import time
import uuid
from datetime import datetime, timedelta
import copy
import os

# third party imports
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from dateutil import parser

# app imports
from driver import firefox_driver_headless
from config import settings


class ErosNowScraper:

    def __init__(self, client_id):
        self.client_id = client_id
        self.base_url = 'https://erosnow.com/'
        self.root_genre = []
        self.genre_items = []
        self.single_genre_items = []
        self.items = []
        self.config = settings.MEDIASENSE_CONFIG.get('erosnow', {})
        self.process_name = 'erosnow_scraper'
        self.base_data_path = '../data/'
        self.path_name = self.create_folder()

    # xx-- General Methods to get elements --xx
    def create_folder(self):
        path_name = self.base_data_path + self.process_name

        if not os.path.exists(path_name):
            os.makedirs(path_name)
        return path_name + "/"

    def write_to_file(self, filename, item_dictionary):
        filename = self.path_name + filename
        with open(filename + ".json", 'a') as f:
            f.write(json.dumps(item_dictionary) + '\n')

    def get_lines(self, filename):
        filename = self.path_name + filename
        with open(filename + ".json", 'r') as f:
            lines = list(
                map(
                    lambda x: json.loads(x.strip()),
                    f.readlines()
                )
            )
        return lines

    def get_element_wait(self, parent_element, wait_time, xpath,
                         single=True, target_attribute=None):
        if xpath is None:
            if target_attribute is None:
                return parent_element
            elif target_attribute == 'text':
                return parent_element.text
            elif target_attribute == 'tagname':
                return parent_element.tagname
            else:
                return parent_element.get_attribute(target_attribute)

        try:
            if single:
                element = WebDriverWait(parent_element, wait_time).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            xpath
                        )
                    )
                )
            else:
                element = WebDriverWait(parent_element, wait_time).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            xpath
                        )
                    )
                )
            if target_attribute is None:
                return element
            elif target_attribute == 'text':
                return element.text
            elif target_attribute == 'tagname':
                return element.tagname
            else:
                return element.get_attribute(target_attribute)
        except Exception as e:
            raise Exception(e)

    def get_element_no_wait(self, parent_element, xpath,
                            single=True, target_attribute=None):
        if xpath is None:
            if target_attribute is None:
                return parent_element
            elif target_attribute == 'text':
                return parent_element.text
            elif target_attribute == 'tagname':
                return parent_element.tagname
            else:
                return parent_element.get_attribute(target_attribute)

        try:
            if single:
                element = parent_element.find_element_by_xpath(
                    xpath
                )
            else:
                element = parent_element.find_elements_by_xpath(
                    xpath
                )
            if target_attribute is None:
                return element
            elif target_attribute == 'text':
                return element.text
            elif target_attribute == 'tagname':
                return element.tagname
            else:
                return element.get_attribute(target_attribute)
        except Exception as e:
            raise Exception(e)

    # xx-- Methods that get all genres urls --xx
    def get_all_root_genres_tags(self, parent_element, config):
        try:
            # load configurations
            xpath = config['xpath']
            wait = config['wait']
            wait_time = config['wait_time']
            target_attribute = config['target_attribute']
            single = config['single']

            if not config:
                return None

            # process page
            if wait:
                return self.get_element_wait(
                    parent_element, wait_time, xpath,
                    single=single, target_attribute=target_attribute)
            else:
                return self.get_element_no_wait(
                    parent_element, xpath,
                    single=single, target_attribute=target_attribute)
        except Exception as e:
            raise Exception(e)

    def get_all_genre_items(self, root_genre_dictionary):
        try:
            url = root_genre_dictionary.get('url', '')
            if not url:
                return []

            driver = firefox_driver_headless.SeleniumWebDriver().driver
            driver.get(url)

            # main div
            main_div_config = copy.deepcopy(
                self.config.get(
                    'genre_page', {}).get('genre_page_main_div', {})
            )
            main_div_absolute = main_div_config.get('absolute', False)
            if main_div_absolute:
                main_div = self.get_all_root_genres_tags(
                    driver, main_div_config)
            else:
                driver.quit()
                return {
                    'Status': 'Error',
                    'Error': 'Incorrect Config: Main Div must be an absolute field'
                }

            if main_div is None:
                driver.quit()
                return {
                    'Status': 'Error',
                    'Error': 'Please provide configurations'
                }

            # need to scroll 3 times
            # on one scroll we get 19 or 20 items.
            scroll_count = 0
            scroll_amount = 500
            while scroll_count <= 10:
                previous_scroll_amount = scroll_amount - 500
                driver.execute_script(
                    'window.scrollTo({},{})'.format(
                        str(previous_scroll_amount),
                        str(scroll_amount)
                    )
                )
                scroll_amount += 500
                scroll_count += 1
                time.sleep(5)

            # link root
            link_root_config = copy.deepcopy(
                self.config.get(
                    'genre_page', {}).get('genre_page_link_root', {})
            )
            link_root_absolute = link_root_config.get('absolute', False)
            if link_root_absolute:
                link_root = self.get_all_root_genres_tags(
                    driver, link_root_config)
            else:
                link_root = self.get_all_root_genres_tags(
                    main_div, link_root_config)

            for link in link_root:
                try:
                    link_config = copy.deepcopy(
                        self.config.get(
                            'genre_page', {}).get('genre_page_link', {})
                    )
                    link_absolute = link_config.get('absolute', True)

                    if link_absolute:
                        url = self.get_all_root_genres_tags(
                            driver, link_config)
                    else:
                        url = self.get_all_root_genres_tags(
                            link, link_config)

                    print('Appending url: ' + url)
                    self.genre_items.append(url)
                    print('Success')

                except Exception as e:
                    print(str(e))
                    continue
            driver.quit()

        except Exception as e:
            raise Exception(e)

    def get_single_genre_items(self, url):
        try:
            driver = firefox_driver_headless.SeleniumWebDriver().driver
            driver.get(url)

            # main div
            main_div_config = copy.deepcopy(
                self.config.get(
                    'genre_page', {}).get('genre_page_main_div', {})
            )
            main_div_absolute = main_div_config.get('absolute', False)
            if main_div_absolute:
                main_div = self.get_all_root_genres_tags(
                    driver, main_div_config)
            else:
                driver.quit()
                return {
                    'Status': 'Error',
                    'Error': 'Incorrect Config: Main Div must be an absolute field'
                }

            if main_div is None:
                driver.quit()
                return {
                    'Status': 'Error',
                    'Error': 'Please provide configurations'
                }

            # the main loop
            link_lower_limit = 0
            link_upper_limit = 0
            while True:
                try:
                    # link root
                    link_root_config = copy.deepcopy(
                        self.config.get(
                            'genre_page', {}).get('genre_page_link_root', {})
                    )
                    link_root_absolute = link_root_config.get(
                        'absolute', False)
                    if link_root_absolute:
                        link_root = self.get_all_root_genres_tags(
                            driver, link_root_config)
                    else:
                        link_root = self.get_all_root_genres_tags(
                            main_div, link_root_config)

                    link = link_root[0]
                    link_config = copy.deepcopy(
                        self.config.get(
                            'genre_page', {}).get(
                                'genre_page_link', {})
                    )
                    link_absolute = link_config.get('absolute', True)

                    if link_absolute:
                        url = self.get_all_root_genres_tags(
                            driver, link_config)
                    else:
                        url = self.get_all_root_genres_tags(
                            link, link_config)

                    print('Appending url: ' + url)
                    self.single_genre_items.append(url)
                    print('Success')

                    # driver.ex

                except Exception as e:
                    print(e)
                    continue
            driver.quit()

        except Exception as e:
            raise Exception(e)

    def get_all_root_genres(self, category_url):
        # main div is the main container
        # link root is the list of all root_genres,
        # which we iterate over
        try:
            # construct url
            url = self.base_url + category_url

            # open url
            driver = firefox_driver_headless.SeleniumWebDriver().driver
            driver.get(url)

            # main div
            main_div_config = copy.deepcopy(
                self.config.get(
                    'root_genres', {}).get('root_genre_main_div', {})
            )
            main_div_absolute = main_div_config.get('absolute', False)
            if main_div_absolute:
                main_div = self.get_all_root_genres_tags(
                    driver, main_div_config)
            else:
                driver.quit()
                return {
                    'Status': 'Error',
                    'Error': 'Incorrect Config: Main Div must be an absolute field'
                }

            if main_div is None:
                driver.quit()
                return {
                    'Status': 'Error',
                    'Error': 'Please provide configurations'
                }

            # link root: this is a list
            link_root_config = copy.deepcopy(
                self.config.get(
                    'root_genres', {}).get('root_genre_link_root', {})
            )
            link_root_absolute = link_root_config.get('absolute', False)
            if link_root_absolute:
                link_root = self.get_all_root_genres_tags(
                    driver, link_root_config)
            else:
                link_root = self.get_all_root_genres_tags(
                    main_div, link_root_config)

            # iterate over the link root and get links
            for link in link_root:
                try:
                    link_config = copy.deepcopy(
                        self.config.get(
                            'root_genres', {}).get('root_genre_link', {})
                    )
                    link_absolute = link_config.get('absolute', True)

                    image_config = copy.deepcopy(
                        self.config.get(
                            'root_genres', {}).get('root_genre_image', {})
                    )
                    image_absolute = image_config.get('absolute', False)

                    root_genre_name_config = copy.deepcopy(
                        self.config.get(
                            'root_genres', {}).get('root_genre_name', {})
                    )
                    root_genre_name_absolute = root_genre_name_config.get(
                        'absolute', False)

                    # get url
                    if link_absolute:
                        url = self.get_all_root_genres_tags(
                            driver, link_config)
                    else:
                        url = self.get_all_root_genres_tags(
                            link, link_config)

                    if image_absolute:
                        image = self.get_all_root_genres_tags(
                            driver, image_config)
                    else:
                        image = self.get_all_root_genres_tags(
                            link, image_config)

                    if root_genre_name_absolute:
                        root_genre = self.get_all_root_genres_tags(
                            driver, root_genre_name_config)
                    else:
                        root_genre = self.get_all_root_genres_tags(
                            link, root_genre_name_config)

                    root_genre_dictionary = {
                        'name': root_genre,
                        'image': image,
                        'url': url
                    }

                    self.root_genre.append(root_genre_dictionary)
                except Exception as e:
                    print(str(e))
                    continue

            # close driver
            print('.....ALL ROOT GENRES HAVE BEEN EXTRACTED.....')
            print(self.root_genre)
            driver.quit()
            return main_div

        except Exception as e:
            driver.quit()
            raise Exception(e)

    # xx-- Heart Scraper Methods --xx
    def filter_urls(self, url_lines):
        filtered_url_list = []

        for url_line in url_lines:
            url = url_line.get('url', '')
            if not url or url == ' ':
                continue

            filtered_url_list.append(url)
        return filtered_url_list

    def get_product_title(self, parent_element):
        title_config = copy.deepcopy(
                self.config.get(
                    'product_page', {}
                ).get('product_page_title', {})
            )

        title = self.get_all_root_genres_tags(
            parent_element, title_config)

        return title

    def image_parser(self, image_string):
        return image_string.split(
            "(")[1].split(")")[0][1:-1]

    def get_product_image(self, parent_element):
        image_config = copy.deepcopy(
                self.config.get(
                    'product_page', {}
                ).get('product_page_image', {})
            )

        image = self.get_all_root_genres_tags(
            parent_element, image_config)

        return self.image_parser(image)

    def date_parser(self, datestring):
        return datetime.strptime(datestring, "%Y").isoformat()

    def get_product_release_date(self, parent_element):
        release_date_config = copy.deepcopy(
                self.config.get(
                    'product_page', {}
                ).get('product_page_release_date', {})
            )

        release_date = self.get_all_root_genres_tags(
            parent_element, release_date_config)

        return self.date_parser(release_date)

    def duration_parser(self, duration_string):
        return int(duration_string.split(" ")[1])

    def get_product_duration(self, parent_element):
        product_duration_config = copy.deepcopy(
                self.config.get(
                    'product_page', {}
                ).get('product_page_duration', {})
            )

        product_duration = self.get_all_root_genres_tags(
            parent_element, product_duration_config)

        return self.duration_parser(product_duration)

    def rating_parser(self, rating_string):
        return int(rating_string.split(
            " ")[-1].split("-")[-1])

    def get_product_rating(self, parent_element):
        rating_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_rating', {})
        )

        rating = self.get_all_root_genres_tags(
            parent_element, rating_config)

        return self.rating_parser(rating)

    def get_product_description(self, parent_element):
        parent_element.execute_script("window.scrollBy(0,500)")
        description_root_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_description_root', {})
        )

        description_root = self.get_all_root_genres_tags(
            parent_element, description_root_config)

        description_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_description', {})
        )

        description = self.get_all_root_genres_tags(
            description_root, description_config)

        return description

    def get_product_hd(self, parent_element):
        try:
            hd_config = copy.deepcopy(
                self.config.get(
                    'product_page', {}
                ).get('product_page_hd', {})
            )

            hd = self.get_all_root_genres_tags(
                parent_element, hd_config)
            return hd
        except:
            return ''

    def get_extra_info(self, parent_element):
        extra_info_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_extra_info_root', {})
        )

        extra_info = self.get_all_root_genres_tags(
            parent_element, extra_info_config)

        return extra_info

    def get_product_cast(self, parent_element):
        # driver is executed first and therefore
        # product cast does not need to
        cast_list = []
        cast_root_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_cast_root', {})
        )
        cast_root = self.get_all_root_genres_tags(
            parent_element, cast_root_config)

        cast_links_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_cast_links', {})
        )
        cast_links = self.get_all_root_genres_tags(
            cast_root, cast_links_config)

        for cast_link in cast_links:
            cast_list.append(cast_link.text)

        return cast_list

    def get_product_director(self, parent_element):
        director_list = []
        director_root_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_director_root', {})
        )

        director_root = self.get_all_root_genres_tags(
            parent_element, director_root_config)

        director_links_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_cast_links', {})
        )

        director_links = self.get_all_root_genres_tags(
            director_root, director_links_config)

        for director_link in director_links:
            director_list.append(director_link.text)

        return director_list

    def get_product_music(self, parent_element):
        music_list = []
        music_root_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_music_root', {})
        )

        music_root = self.get_all_root_genres_tags(
            parent_element, music_root_config)

        music_links_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_music_links', {})
        )

        music_links = self.get_all_root_genres_tags(
            music_root, music_links_config)

        for music_link in music_links:
            music_list.append(music_link.text)

        return music_list

    def get_product_language(self, parent_element):
        language_root_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_language_root', {})
        )

        language_root = self.get_all_root_genres_tags(
            parent_element, language_root_config)

        language_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_language', {})
        )

        language = self.get_all_root_genres_tags(
            language_root, language_config)

        return language

    def get_product_genre(self, parent_element):
        genre_list = []
        genre_root_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_genre_root', {})
        )

        genre_root = self.get_all_root_genres_tags(
            parent_element, genre_root_config)

        genre_links_config = copy.deepcopy(
            self.config.get(
                'product_page', {}
            ).get('product_page_genre_links', {})
        )

        genre_links = self.get_all_root_genres_tags(
            genre_root, genre_links_config)

        for genre_link in genre_links:
            genre_list.append(genre_link.text)

        return genre_list

    def erosnow_product_scraper(self, url):
        try:
            driver = firefox_driver_headless.SeleniumWebDriver().driver
            driver.get(url)

            # process the page here
            title = self.get_product_title(driver)
            image = self.get_product_image(driver)
            release_date = self.get_product_release_date(driver)
            product_duration = self.get_product_duration(driver)
            rating = self.get_product_rating(driver)
            description = self.get_product_description(driver)
            hd = self.get_product_hd(driver)

            # this one is for info like: cast, director
            # we need to first get extra_info tag
            # which will act as a parent element for everything forward
            extra_info = self.get_extra_info(driver)

            cast = self.get_product_cast(extra_info)
            director = self.get_product_director(extra_info)
            music = self.get_product_music(extra_info)
            language = self.get_product_language(extra_info)
            genre = self.get_product_genre(extra_info)

            item_dictionary = {
                'title': title,
                'image': image,
                'release_date': release_date,
                'product_duration': product_duration,
                'rating': rating,
                'description': description,
                'quality': hd,
                'cast': cast,
                'director': director,
                'music': music,
                'language': language,
                'genre': genre,
            }

            self.write_to_file('erosnow_intermediatory_file', item_dictionary)
            driver.quit()

            return item_dictionary
        except Exception as e:
            raise Exception(e)

    # turning this to a batch now
    def collect_url(self, root_genre=''):
        if not root_genre:
            try:
                # get all genre urls
                self.get_all_root_genres('movies/genres')

                # for each genre url, get product page url
                for root_genre_dictionary in self.root_genre:
                    self.get_all_genre_items(root_genre_dictionary)
                self.genre_items = list(set(self.genre_items))
                # write product page url into a file
                for item in self.genre_items:
                    item_dict = {
                        'url': item
                    }
                    self.write_to_file('erosnow_product_urls_new', item_dict)
            except Exception as e:
                raise Exception(e)
        else:
            try:
                self.get_all_root_genres('movies/genres')

                # construct a dictionary
                root_genre_dictionary = {}
                for genre_dictionary in self.root_genre:
                    genre_name = genre_dictionary.get('name', '').lower()
                    genre_url = genre_dictionary.get('url', '')
                    root_genre_dictionary[genre_name] = genre_url
                
                url = root_genre_dictionary[root_genre]
                self.get_single_genre_items(url)                

            except Exception as e:
                raise Exception(e)

    # turning this to a batch now
    def format_data(self):
        try:
            # read from that file
            url_lines = self.filter_urls(
                self.get_lines('erosnow_product_urls_new'))
            for url_line in url_lines:
                try:
                    url_category = url_line.split('/')[3]
                    if url_category not in ['movie']:
                        continue
                    item_dictionary = self.erosnow_product_scraper(url_line)
                    print(item_dictionary)
                    self.items.append(item_dictionary)
                    self.write_to_file(
                        'erosnow_intermediatory_file_new',
                        item_dictionary
                    )
                except Exception as e:
                    print(str(e))
                    continue
        except Exception as e:
            raise Exception(e)

    def __call__(self):
        try:
            # self.collect_url(root_genre='action')    
            self.format_data()
        except Exception as e:
            raise Exception(e)
