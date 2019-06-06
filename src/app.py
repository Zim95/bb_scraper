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

DROPDOWN_CLASS = 'meganav-shop'
DROPDOWN_MENU_CLASS = 'dropdown-menu'
ITEM_DIV_CLASS = 'items'
DEFAULT_ITEM_COUNT = 20


def read_from_file():
    with open('../data/modified_urls.json', 'r') as f:
        lines = f.readlines()
    return lines


def write_to_file(dictionary):
    with open('../data/modified_data4.json', 'a') as f:
        f.write(json.dumps(dictionary)+"\n")
    return


def get_offer(driver, div_for_offer):
    offer_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, './/product-template/div/div[2]/div[2]/div/div')
            )
        )

    return offer_div.text


def get_link_to_main_page(item):
    link_to_main_page = item.find_element_by_xpath(
            ".//product-template/div/div[3]/a"
        ).get_attribute('href')
    return link_to_main_page


def get_small_image_source(item):
    small_image_source = item.find_element_by_xpath(
            ".//product-template/div/div[3]/a/img"
        ).get_attribute('src')
    return small_image_source


def get_brand_name(item):
    brand_div = item.find_element_by_xpath(
        ".//product-template/div/div[4]/div[1]"
    )
    brand = brand_div.find_element_by_xpath(
        ".//h6"
    ).text
    name = brand_div.find_element_by_xpath(
        ".//a"
    ).text
    return brand, name


def get_currency_price(item):
    mrp_price = item.find_element_by_xpath(
        ".//product-template/div/div[4]/div[3]/div/div[1]/h4/span[1]/span"
    ).text
    return mrp_price


def scrape():
    lines = read_from_file()
    item_id_start = 83

    for line in lines:

        json_line = json.loads(line)

        url = json_line['link']
        label = json_line['label'].split("/")[6]
        primary_category = json_line['prim_cat_key']
        sub_category = json_line['sub_cat']

        driver_obj = firefox_driver_headless.SeleniumWebDriver()
        driver = driver_obj.driver
        driver.get(url)

        item_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.' + ITEM_DIV_CLASS)
            )
        )

        number_of_items_input = driver.find_element_by_id(
            "snowplow_screen_view_totalcount"
        )

        number_of_items = int(number_of_items_input.get_attribute('value'))

        number_of_scrolls = int(number_of_items/DEFAULT_ITEM_COUNT)
        print(number_of_scrolls)

        for i in range(number_of_scrolls + 1):
            print('scroll: ' + str(i))
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(10)

        all_item_divs = item_div.find_elements_by_xpath(
            './/following-sibling::div[contains(@class, "item")]')

        if len(all_item_divs) > 8:
            all_item_divs = all_item_divs[:8]

        for item in all_item_divs:
            try:
                brand, name = get_brand_name(item)
                link_to_main_page = get_link_to_main_page(item)
                small_image = get_small_image_source(item)

                item_dict = {
                    'item_id': str(item_id_start),
                    'title': name,
                    'images': {
                        'small_image': small_image,
                        'thumbnail': small_image,
                        'featured_image': small_image,
                    },
                    'brand': brand,
                    'manufacturer': '',
                    'category_trees': [
                        {
                            'label': '{}/{}/{} {}'.format(
                                primary_category,
                                sub_category,
                                label,
                                name
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
                    "product_links": [link_to_main_page],
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
                    "rating": ""
                }

                driver_obj2 = firefox_driver_headless.SeleniumWebDriver()
                driver2 = driver_obj2.driver
                driver2.get(url)
                driver2.get(link_to_main_page)

                # wait for something to load
                base_image_tag = WebDriverWait(driver2, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/img"
                        )
                    )
                )
                base_image = base_image_tag.get_attribute('src')

                price_tag = driver2.find_element_by_xpath(
                    "/html/body/div[1]/div/div[2]/div[2]/div[3]/div[1]/div/div/div/table/tbody/tr[1]/td[2]"
                ).text
                
                price = float(price_tag.split(" ")[1])
                currency = price_tag.split(" ")[0]

                long_description = driver2.find_element_by_xpath(
                    "/html/body/div[1]/div/div[2]/div[2]/div[3]/div[1]/h1"
                ).text

                if 'Combo' in long_description or 'combo' in long_description or '+' in long_description:
                    continue
                item_dict['price'] = price
                item_dict['currency'] = currency
                item_dict['images']['base_image'] = base_image
                item_dict['long_description'] = long_description
                item_dict['short_description'] = long_description

                write_to_file(item_dict)

                driver2.quit()

                item_id_start = item_id_start + 1
            except Exception:
                item_id_start = item_id_start + 1
                continue

        driver.quit()


def main():
    scrape()

if __name__ == "__main__":
    main()
