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

# app imports
from driver import firefox_driver_headless


def read_from_file():
    with open('../data/mobile_urls.json', 'r') as f:
        lines = f.readlines()
    return lines


def write_to_file(dictionary):
    with open('../data/armani_apparel_data.json', 'a') as f:
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


def scrape():
    item_id = 3785
    lines = [
        { 
            "url": "https://www.armani.com/in/armanicom/giorgio-armani/women/suits-combined",
            "cat": "suits",
            "scroll_count": 400,
            "wait_time": 18,
            "scroll_item_limit": 1200,
            "scroll_item_amount": 1200
        },
    ]

    for url in lines:

        driver_obj = firefox_driver_headless.SeleniumWebDriver()
        driver = driver_obj.driver
        driver.get(url['url'])

        try:
            primary_category = 'women'

            secondary_category = 'womens-clothing'

            leaf_category = url['cat']

            print('Primary Category: ' + primary_category)
            print('Secondary Category: ' + secondary_category)
            print('Leaf Category: ' + leaf_category)

            driver.execute_script(
                        'window.scrollTo({},{})'.format(
                                    '0',
                                    str(url['scroll_count'])
                                )
                    )

            # hide_banner_btn = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (
            #             By.XPATH,
            #             '/html/body/div[1]/div[1]/div[2]/div[1]/div/button'
            #         )
            #     )
            # )

            # hide_banner_btn.click()

            item_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '/html/body/div[3]/main/div/div/section[1]/div[1]/div/ul'
                    )
                )
            )

            print('Got main div tag....')
            print(item_div.tag_name)

            time.sleep(url['wait_time'])

            item_list = item_div.find_elements_by_xpath(
                './/article'
            )

            print('Got item list....')
            print(len([item.tag_name for item in item_list]))
            # print('item list count: ' + str(len(item_list)))

            SCROLL_ITEM_LIMIT = url['scroll_item_limit']
            SCROLL_ITEM_AMOUNT = url['scroll_item_amount']

            for item in item_list:
                try:
                    # img_tag = WebDriverWait(item, 10).until(
                    #     EC.presence_of_element_located(
                    #         (
                    #             By.XPATH,
                                
                    #         )
                    #     )
                    # )
                    img_tag = item.find_element_by_xpath(
                        './/a/figure/div[3]/img'
                    )

                    small_image = img_tag.get_attribute('data-origin')

                    print('Got image: ' + small_image)

                    # title_tag = WebDriverWait(item, 10).until(
                    #     EC.presence_of_element_located(
                    #         (
                    #             By.XPATH,
                    #             './/div/div/div/a/div'
                    #         )
                    #     )
                    # )
                    title_tag = item.find_element_by_xpath(
                        './/a/div/div/span'
                    )

                    title = title_tag.text
                    print('Got title: ' + title)

                    brand = 'Armani'
                    print('Got brand: ' + brand)

                    price_tag = item.find_element_by_xpath(
                        './/div/div/div[1]/div/span/span[2]'
                    )
                    price = float(price_tag.text.replace(',', ''))
                    print(price)

                    item_dict = {
                        'item_id': str(item_id),
                        'title': title,
                        'images': {
                            'small_image': small_image,
                            'thumbnail': small_image,
                            'featured_image': small_image,
                        },
                        'brand': brand,
                        'manufacturer': '',
                        'category_trees': [
                            {
                                'label': '{}/{}/{}'.format(
                                    primary_category,
                                    secondary_category,
                                    leaf_category
                                ),
                                'is_primary': True
                            }
                        ],
                        "item_type": "parent",
                        "parent_id": 0,
                        "visibility": {
                            "visible_in_catalog": True,
                            "visible_in_search": True
                        },
                        "in_stock": 1,
                        "product_links": [],
                        "product_attributes": [],
                        "accessories": {},
                        "features": {},
                        "product_services": {},
                        "reviews": [],
                        "associated_item_ids": [],
                        "manufacturer": "",
                        "tags": [],
                        "sku": "",
                        "classification": "",
                        "rating": "",
                        "price": price,
                        "currency": "USD",
                        "long_description": title,
                        "short_description": title
                    }

                    write_to_file(item_dict)

                    item_id = item_id + 1

                    # scroll and then continue
                    driver.execute_script(
                        'window.scrollTo({},{})'.format(
                                        str(
                                            SCROLL_ITEM_LIMIT - SCROLL_ITEM_AMOUNT
                                        ),
                                        str(SCROLL_ITEM_LIMIT)
                                    )
                    )
                    SCROLL_ITEM_LIMIT = SCROLL_ITEM_LIMIT + SCROLL_ITEM_AMOUNT
                except Exception as e:
                   print(e)
                   continue
        except Exception as e:
            print(str(e))
            continue

        driver.quit()


def main():
    scrape()


if __name__ == "__main__":
    main()
