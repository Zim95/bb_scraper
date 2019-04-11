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
import copy
import time
import json

# app imports
from driver import firefox_driver_headless

DROPDOWN_CLASS = 'meganav-shop'
DROPDOWN_MENU_CLASS = 'dropdown-menu'
ITEM_DIV_CLASS = 'items'
DEFAULT_ITEM_COUNT = 20


def write_to_file(dictionary):
    with open('../data/all_urls.json', 'w') as f:
        for key, value in dictionary.items():
            f.write(json.dumps(value) + '\n')


def get_offer(driver, div_for_offer):
    offer_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, './/product-template/div/div[2]/div[2]/div/div')
            )
        )

    return offer_div.text


def scrape(driver, leaf_category_list):
    for key, value in leaf_category_list.items():
        category_tree = key
        url = value['link']
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

        print(len(all_item_divs))

        return


def process_subcategory(sub_category):
    sub_category_dictionary = {}

    sub_category_list = sub_category.find_elements_by_xpath(
        './/li'
    )

    for sub_category in sub_category_list:
        a_tag = sub_category.find_element_by_xpath('.//a')

        a_link_text = a_tag.text
        a_link_value = a_tag.get_attribute('href')
        dictionary_key = '-'.join(a_link_text.lower().split(' '))

        sub_category_dictionary[dictionary_key] = {
            'link': a_link_value,
            'label': a_link_value,
            'selenium_a_item': a_tag,
            'selenium_list_item': sub_category
        }

    return sub_category_dictionary


def process_leafcategory(leaf_category, sub_cat_key, prim_cat_key):
    leaf_category_dictionary = {}

    leaf_category_list = leaf_category.find_elements_by_xpath(".//li")

    for leaf_category in leaf_category_list:
        a_tag = leaf_category.find_element_by_xpath('.//a')

        a_link_text = a_tag.text
        a_link_value = a_tag.get_attribute('href')
        dictionary_key = '-'.join(a_link_text.lower().split(' '))

        leaf_category_dictionary[dictionary_key] = {
            'link': a_link_value,
            'label': a_link_value,
            'sub_cat': sub_cat_key,
            'prim_cat_key': prim_cat_key
        }

    return leaf_category_dictionary


def process_partial_leafcategory(driver, primary_cat):
    leaf_category = {}
    if primary_cat == 'None' or primary_cat is None:
        return

    div_for_leaf_cat = driver.find_element_by_id(primary_cat)
    leaf_cat_ul = div_for_leaf_cat.find_element_by_xpath(
        ".//div/div/div[2]/div/div/div/div/div/ul"
    )
    leaf_cat_li = leaf_cat_ul.find_elements_by_xpath(
        ".//li"
    )

    for item in leaf_cat_li:
        a_tag = item.find_element_by_xpath(
            ".//a"
        )

        a_link_value = a_tag.get_attribute('href')
        a_link_text = a_link_value.split('/')[6]
        sub_cat = a_link_value.split('/')[5]
        key = primary_cat + "/" + sub_cat + "/" + a_link_text

        leaf_category[key] = {
            'link': a_link_value,
            'text': a_link_text,
            'primary_category': primary_cat,
            'sub_category': sub_cat
        }

    return leaf_category


def get_list_of_sub_category(driver, primary_category_list):
    sub_category_list = {}

    for key, value in primary_category_list.items():
        primary_key = key
        selenium_list_item = value['selenium_list_item']
        selenium_a_item = value['selenium_a_item']

        hover_list = ActionChains(driver).move_to_element(selenium_list_item)
        hover_list.perform()

        hover_a = ActionChains(driver).move_to_element(selenium_a_item)
        hover_a.perform()

        sub_category = driver.find_element_by_xpath(
            '//li/mega-nav-template/div/div/div/left-subcategory-template/div/div/div/div[1]/ul'
        )

        sub_category_dictionary = process_subcategory(sub_category)

        sub_category_list[primary_key] = sub_category_dictionary

    return sub_category_list


def get_list_of_leaf_category(
                    driver, primary_category_list, sub_category_list):
    import pdb; pdb.set_trace()
    leaf_category_list = {}

    for primary_cat, sub_categories in sub_category_list.items():
        try:
            primary_selenium_list_item = primary_category_list[primary_cat][
                    'selenium_list_item']
            primary_selenium_a_item = primary_category_list[primary_cat][
                    'selenium_a_item']

            primary_hover_list = ActionChains(driver).move_to_element(
                    primary_selenium_list_item)
            primary_hover_list.perform()

            primary_hover_a = ActionChains(driver).move_to_element(
                    primary_selenium_a_item)
            primary_hover_a.perform()

            sub_category = driver.find_element_by_xpath(
                '//li/mega-nav-template/div/div/div/left-subcategory-template/div/div/div/div[1]/ul'
            )

            sub_category_list = sub_category.find_elements_by_xpath(
                './/li'
            )

            for sub_cat in sub_category_list:
                a_tag = sub_cat.find_element_by_xpath(
                    ".//a"
                )

                sub_hover_list = ActionChains(driver).move_to_element(
                    sub_cat)
                sub_hover_list.perform()

                sub_hover_a = ActionChains(driver).move_to_element(
                        a_tag)
                sub_hover_a.perform()

                sub_cat_text = '-'.join(a_tag.text.lower().split(' '))

                leaf_category = driver.find_element_by_xpath(
                    "//li/mega-nav-template/div/div/div/left-subcategory-template/div/div/div/div[2]/div/div/div/div[1]/div/ul"
                )

                leaf_category_dictionary = process_leafcategory(
                    leaf_category, sub_cat_text, primary_cat)

                print(leaf_category_dictionary)

                leaf_category_list.update(leaf_category_dictionary)
            # leaf_cat = process_partial_leafcategory(driver, primary_cat)

            # leaf_category_list.update(leaf_cat)
        except Exception:
            continue

    return leaf_category_list


def main(url=None):
    if url is None:
        return

    driver_obj = firefox_driver_headless.SeleniumWebDriver()
    driver = driver_obj.driver
    driver.get(url)

    # wait for the dropdown to appear

    # soup = BeautifulSoup(driver.page_source, 'lxml')
    product_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a.' + DROPDOWN_CLASS)
        )
    )

    hover = ActionChains(driver).move_to_element(product_dropdown)
    hover.perform()

    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'ul.' + DROPDOWN_MENU_CLASS)
        )
    )

    # print(dropdown_menu.get_attribute('class'))

    all_categories_list = dropdown_menu.find_elements_by_xpath(
        '//li/mega-nav-template/div/ul/*')

    primary_category_list = {}

    for list_item in all_categories_list:
        if list_item is None:
            continue

        dictionary_key = list_item.get_attribute('data-submenu-id')

        if not dictionary_key:
            continue

        a_tag = list_item.find_elements_by_xpath('.//a')[0]
        a_link_value = a_tag.get_attribute('href')
        a_link_text = a_tag.text

        primary_category_list[dictionary_key] = {
            'link': a_link_value,
            'label': a_link_text,
            'selenium_list_item': list_item,
            'selenium_a_item': a_tag
        }

    sub_category_list = get_list_of_sub_category(
        driver, primary_category_list)

    leaf_category_list = get_list_of_leaf_category(
        driver, primary_category_list, sub_category_list
    )

    # scrape(driver, leaf_category_list)
    write_to_file(leaf_category_list)

    driver.quit()


if __name__ == "__main__":
    main(url='https://www.bigbasket.com/')
