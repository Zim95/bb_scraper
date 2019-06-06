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
import json
import time
from datetime import datetime

# third-party imports
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

# app imports
from driver import firefox_driver_headless
from config import settings


class BaseMediaSenseNewsScraper:

    def __init__(self, config, process_name, root_url='', run_local=True):
        self.run_local = run_local
        self.process_name = process_name
        self.config_dictionary = settings.MEDIASENSE_CONFIG[config]
        self.local_url_prefix = ''
        self.production_url_prefix = ''
        self.root_url = root_url

        driver_obj = firefox_driver_headless.SeleniumWebDriver()
        self.driver = driver_obj.driver
        self.url_list = []

    def construct_intermediate_write_filename(self):
        return '../data/{}_data.json'.format(
            self.process_name)

    def construct_write_filename(self):
        if self.run_local:
            prefix = "local"
        else:
            prefix = "production"
        return '../data/{}_{}_data.json'.format(
            prefix,
            self.process_name
        )

    def write_to_file(self, filename, item_dictionary):
        with open(filename, 'a') as f:
            f.write(json.dumps(item_dictionary) + "\n")

    def get_urls_selenium_item_div(self, parent_element):
        wait_time = self.config_dictionary[
            'get_urls']['main_item_div']['wait_time']

        if self.config_dictionary['get_urls']['main_item_div']['wait']:
            item_div = WebDriverWait(parent_element, wait_time).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.config_dictionary[
                            "get_urls"]["main_item_div"]["xpath"]
                    )
                )
            )
        else:
            item_div = parent_element.find_element_by_xpath(
                self.config_dictionary[
                    "get_urls"]["main_item_div"]["xpath"]
            )
        return item_div

    def get_urls_selenium_item_list(self, parent_element):
        wait_time = self.config_dictionary[
            'get_urls']['item_list']['wait_time']

        if self.config_dictionary['get_urls']['item_list']['wait']:
            item_list = WebDriverWait(parent_element, wait_time).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        self.config_dictionary['get_urls']['item_list']['xpath']
                    )
                )
            )
        else:
            item_list = parent_element.find_elements_by_xpath(
                self.config_dictionary['get_urls']['item_list']['xpath']
            )
        return item_list

    def get_urls_selenium(self):
        # if self.root_url is empty this means we take data
        # from file
        if not self.root_url:
            return

        # we create a copy so that the real driver is not shut down
        # upon quit
        driver = self.driver
        driver.get(self.root_url)

        item_div = self.get_urls_selenium_item_div(driver)

        if self.config_dictionary['get_urls']['item_list']['absolute']:
            item_list = self.get_urls_selenium_item_list(driver)
        else:
            item_list = self.get_urls_selenium_item_list(item_div)

        for item in item_list:
            try:
                item_source = item.find_element_by_xpath(
                    ".//div/article/div[2]/div/a"
                )

                source = item_source.text
                if source in ['Reuters', 'Reuters India', 'Fox News']:
                    article_url = item.find_element_by_xpath(
                        ".//div/article/h3/a"
                    )
                    item_url = article_url.get_attribute('href')
                    self.url_list.append(item_url)

            except Exception as e:
                print('Error: ' + str(e))
                continue

        driver.quit()
        return self.url_list

    def get_urls_file(self):
        # virual function
        pass

    def scrape(self):
        # virtual function
        pass

    def collect_item_dictionary(self):
        # virtual function
        pass

    def convert_data(self, item_dictionary):
        provider = item_dictionary.get("client_id", "")
        item_id = item_dictionary.get('item_id', '')
        if not provider:
            return {}
        if not item_id:
            return {}

        strfstring = "%Y:%m:%dT%H:%M:%S.%fZ"
        cast = item_dictionary.get('cast', [])
        pid = item_dictionary.get('pid', {})
        category = [item_dictionary.get('category', '')]
        release_decades = item_dictionary.get('release_decades', '')
        showname = item_dictionary.get('showname', '')
        published_at = item_dictionary.get('published_at', '')

        starts_at = datetime.strftime(
            item_dictionary.get('schedule', {}).get('starts_at', ''),
            strfstring
        ) if item_dictionary.get('schedule', {}).get('starts_at', '') else ''
        ends_at = datetime.strftime(
            item_dictionary.get('schedule', {}).get('ends_at'),
            strfstring
        ) if item_dictionary.get('schedule', {}).get('ends_at', '') else ''
        schedule = {
            'ends_at': ends_at,
            'starts_at': starts_at
        }

        release_date = datetime.strftime(
            item_dictionary.get('release_date', ''),
            strfstring
        ) if item_dictionary.get('release_date', '') else ''
        last_modified = datetime.strftime(
            datetime.utcnow(),
            strfstring
        )

        tags = item_dictionary.get('tags', '')
        is_searchable = item_dictionary.get('is_searchable', '')
        item_type = item_dictionary.get('item_type', '')

        state = 'active'
        language = item_dictionary.get('language', '')
        genre = item_dictionary.get('genre', '')

        metadata = item_dictionary.get('metadata', {})
        image = metadata.get(
            'images', {}).get(
                'thumbnail', {}).get(
                    'src', '') if metadata else ''
        title = metadata.get('name', '') if metadata else ''
        description = metadata.get('description') if metadata else ''
        kg_cast = item_dictionary.get('kg_cast', {})
        kg_update = item_dictionary.get('kg_update', False)

        item_dict = {
            "client_id": provider, "item_id": item_id, "cast": cast,
            "category": category, "description": description,
            "extra": {"pid": pid}, 'recosense_metadata': {
                'annotation': kg_cast, 'tags': tags},
            "genres": [genre], "image": image, "item_list_type": genre,
            "item_type": item_type, "kg_update": kg_update,
            "is_searchable": is_searchable, "language": language,
            "last_modified": last_modified, "published_date": published_at,
            "release_decades": release_decades, "released_date": release_date,
            "schedule": schedule, "showname": showname, "state": state,
            "title": title,
        }

        return item_dict


class ReuterMediaSenseNewsScraper(BaseMediaSenseNewsScraper):

    def __init__(self, root_url='', run_local=True):
        self.process_name = 'mediasense_news_reuter'
        self.root_url = root_url
        self.config = 'reuter'
        self.url_list = []

        super().__init__(
            self.config, self.process_name, self.root_url, run_local)
    
    def get_title_text(self, parent_element):
        # get title tag
        title_tag_rules = self.config['item_dictionary']['title_tag']
        wait_time = title_tag_rules['wait_time']

        if title_tag_rules['wait']:
            title_tag = WebDriverWait(parent_element, wait_time).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        title_tag_rules['xpath']
                    )
                )
            )
        else:
            title_tag = parent_element.find_element_by_xpath(
                title_tag_rules['xpath']
            )
        title = title_tag.text

        return title

    def get_description_text(self, parent_element):
        description_tag_rules = self.config['item_dictionary']['description_tag']
        wait_time = description_tag_rules['wait_time']

        if description_tag_rules['wait']:
            description_tag = WebDriverWait(parent_element, wait_time).until(
                EC.presence_of_element_located(
                    (
                            By.XPATH,
                            description_tag_rules['xpath']
                    )
                )
            )
        else:
            description_tag = parent_element.find_element_by_xpath(
                description_tag_rules['xpath']
            )

        description = description_tag.text

        return description

    def reuter_image_parser(self, image_string):
        return image_string

    def get_image(self, parent_element):
        image_tag_rules = self.config['item_dictionary']['image_tag']
        wait_time = image_tag_rules['wait_time']

        if image_tag_rules['wait']:
            image_tag = WebDriverWait(parent_element, wait_time).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        image_tag_rules['xpath']
                    )
                )
            )
        else:
            image_tag = parent_element.find_element_by_xpath(
                image_tag_rules['xpath']
            )
        image = self.reuter_image_parser(image_tag.get_attribute('style'))
        return image

    def reuter_date_parser(self, datestring):
        return datestring

    def get_date_string(self, parent_element):
        date_tag_rules = self.config['item_dictionary']['published_at_tag']
        wait_time = date_tag_rules['wait_time']
        
        if date_tag_rules['wait']:
            date_tag = WebDriverWait(parent_element, wait_time).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        date_tag_rules['xpath']
                    )
                )
            )
        else:
            date_tag = parent_element.find_element_by_xpath(
                date_tag_rules['xpath']
            )
        date = date_tag.text
        return date

    def collect_item_dictionary(self, url_list):
        # the driver used here has already opened a url
        # this driver will be used to get item_dictionary
        # and has to be passed from some other function
        driver = self.driver

        item_dictionary_list = []
        for url in url_list:
            item_dictionary = {}
            # to be discussed 
            item_id = ''
            client_id = ''

            title = self.get_title_text(driver)
            description = self.get_description_text(driver)
            image = self.get_image(driver)
            date = self.reuter_date_parser(
                self.get_date_string(driver)
            )
            
            item_dictionary['client_id'] = client_id
            item_dictionary['item_id'] = item_id
            item_dictionary['title'] = title
            item_dictionary['description'] = description
            item_dictionary['date'] = date

            item_dictionary_list.append(item_dictionary)

        driver.quit()
        return item_dictionary

    def __call__(self):

        driver = self.driver
        driver.get(self.root_url)

        url_list = self.get_urls_selenium()
        item_dictionary = self.collect_item_dictionary(url_list)

        for item_dict in item_dictionary:
            item_dict_converted = self.convert_data(item_dictionary)
            intermediate_file = self.construct_intermediate_write_filename()
            self.write_to_file(intermediate_file, item_dict)
