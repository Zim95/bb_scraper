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
    with open('../data/new_mobile_data.json', 'a') as f:
        f.write(json.dumps(dictionary)+"\n")
    return


def convert_to_usd(price):
    amount = 0
    for character in price:
        if character in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            amount = (amount * 10) + int(character)
        else:
            continue
    return amount*0.014


def scrape():
    lines = []
    price_range = [
        ['Min', '2000'],
        ['2000', '4000'],
        ['4000', '7000'],
        ['7000', '10000'],
        ['10000', '13000'],
        ['13000', '16000'],
        ['16000', '20000'],
        ['20000', '25000'],
        ['25000', '30000'],
        ['30000', '50000'],
        ['50000', 'Max']
    ]
    base_url = 'https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_1_0&otracker1=AS_Query_TrendingAutoSuggest_1_0&as-pos=1&as-type=TRENDING&p%5B%5D=facets.price_range.from%3D{}&p%5B%5D=facets.price_range.to%3D{}&p%5B%5D=facets.serviceability%5B%5D%3Dtrue'

    for prange in price_range:
        lines.append(base_url.format(prange[0], prange[1]))

    item_id = 517

    for url in lines:

        driver_obj = firefox_driver_headless.SeleniumWebDriver()
        driver = driver_obj.driver
        driver.get(url)

        item_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div._1HmYoV:nth-child(2)')
            )
        )

        item_list = driver.find_elements_by_xpath('/html/body/div/div/div[3]/div[2]/div/div/div[2]/div')

        count = 50
        for index, item in enumerate(item_list):
            try:
                if index == 0:
                    continue

                print('item_id: ' + str(item_id) + ', wating for item to appear..')
                img_tag = WebDriverWait(item, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, './/div/div/div/a/div[2]/div[1]/div[1]/div/img')
                    )
                )
                print('img class: ' + img_tag.get_attribute('class'))
                image = img_tag.get_attribute('src')
                
                # for svg case
                img_ext = image.split(".")[-1]
                print('img_extension: ' + img_ext)

                if img_ext == 'svg':
                    # import pdb; pdb.set_trace()
                    while img_ext == 'svg':
                        print('...............iteration................' + str(count))
                        # driver.execute_script(
                        #     'window.scrollTo(0, parseInt({} * 0.20 * document.body.scrollHeight));'.format(
                        #         str(count+1)
                        #     )
                        # )
                        driver.execute_script(
                            'window.scrollTo({}, {});'.format(
                                str(count - 50),
                                str(count)
                            )
                        )

                        img_tag = WebDriverWait(item, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, './/div/div/div/a/div[2]/div[1]/div[1]/div/img')
                                    )
                                )

                        print('img class: ' + img_tag.get_attribute('class'))
                        image = img_tag.get_attribute('src')
                        img_ext = image.split(".")[-1]
                        count = count + 50
                        time.sleep(1)

                print('item_id: ' + str(item_id) + ', got image..')
                print('image_url: ' + str(image))

                title_tag = WebDriverWait(item, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, './/div/div/div/a/div[3]/div[1]/div[1]')
                    )
                )

                title = title_tag.text
                brand = title.split(" ")[0].lower()

                print('item_id: ' + str(item_id) + ', got title and brand..')
                print('title: ' + title)
                print('brand: ' + brand)

                price_tag = WebDriverWait(item, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, './/div/div/div/a/div[3]/div[2]/div[1]/div/div[1]')
                    )
                )

                price = price_tag.text


                print('item_id: ' + str(item_id) + ', got price..')

                primary_category = 'electronics'
                secondary_category = 'mobiles'
                leaf_category = brand

                category_trees = '{}/{}/{}'.format(
                    primary_category,
                    secondary_category,
                    leaf_category
                )

                
                print('item_id: ' + str(item_id) + ', completed all data scraping..')

                item_data = {
                    'item_id': str(item_id),
                    'title': title,
                    'images': {
                        'small_image': image,
                        'thumbnail': image,
                        'featured_image': image,
                    },
                    'brand': brand,
                    'manufacturer': brand,
                    'category_trees': [
                        {
                            'id': category_trees,
                            'label': category_trees,
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
                    "price": convert_to_usd(price),
                    "currency": "USD",
                    "long_description": title,
                    "short_description": title
                }

                print('item_id: ' + str(item_id) + ', constructed data, waiting to write..')

                write_to_file(item_data)

                print('item_id: ' + str(item_id) + ', successfully written to file..')

                item_id += 1

            except Exception as e:
                print('ERROR FOR NO REASON')
                print(str(e))
                continue

        driver.quit()


def main():
    scrape()

if __name__ == "__main__":
    main()
