#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 root <root@namah>
#
# Distributed under terms of the MIT license.

"""
Description: An image downloader python code
Author: NamahRecoSense
"""

import requests
import json
import os

DEFAULT_COUNT = 1
LOCALHOST_IMAGE_URL = 'http://localhost/repositories/Retailsense-Saas-dashboard/'
PRODUCTION_IMAGE_URL = 'https://retailsense.recosenselabs.com/'

COMMON_IMAGE_URL = 'retaildemo-views/retaildemo/static/assets/images/rsRetail/'


def download_image(folder_name=None, image_name=None, image_ext=None, image_url=None):
    if image_url is None or image_url == 'None':
        return

    image_data = requests.get(image_url).content

    if folder_name is None:
        folder_name = 'default'
    if image_ext is None:
        image_ext = '.jpg'
    if image_name is None:
        image_name = 'default' + str(DEFAULT_COUNT) + image_ext
        DEFAULT_COUNT = DEFAULT_COUNT + 1
    if not os.path.exists('images/' + folder_name):
        os.makedirs('images/' + folder_name)

    try:
        with open('images/' + folder_name+'/'+image_name+image_ext, 'wb') as img_handler:
            img_handler.write(image_data)

        return folder_name + "/" + image_name+image_ext
    except Exception as e:
        print(e)
        return


def remove_null(string):
    string_list = list(filter(lambda x: x not in ['', '-'], string.split('-')))
    return '-'.join(string_list)


def remove_special_characters_label(label):
    label = label.replace(',', '')
    label = label.replace('&', '')
    return label


def parse_line(json_line):
    image_url = json_line['images']['small_image']
    label_string = remove_null(
        remove_special_characters_label(
            json_line['category_trees'][0]['label']
        )
    )
    label_list = label_string.split("/")
    primary_category = label_list[0]
    sub_category = label_list[1]
    leaf_category_label = label_list[2]
    leaf_category = leaf_category_label.split(" ")[0]
    label = '_'.join(leaf_category_label.split(" ")[1:])

    return primary_category, sub_category, leaf_category, label, image_url


def replace_delimiter(delimiter, string):
    string_list = string.split(delimiter)
    return '_'.join(string_list)


def write_data(dictionary):
    with open('./production_data.json', 'a') as f:
        f.write(json.dumps(dictionary) + "\n")


def read_data():
    with open('./backup_modified_data.json', 'r') as f:
        lines = f.readlines()

    for line in lines:
        json_line = json.loads(line)
        primary_category, sub_category, leaf_category, label, img_url = parse_line(json_line)
        folder_name = replace_delimiter('-', primary_category)+'/' +replace_delimiter('-', sub_category) +'/'+ replace_delimiter('-', leaf_category)
        image_name = replace_delimiter(' ', label)
        img_extension = "." + img_url.split(".")[-1]
        url = download_image(
            folder_name=folder_name,
            image_name=image_name,
            image_ext=img_extension,
            image_url=img_url
        )
        json_line['images']['small_image'] = PRODUCTION_IMAGE_URL + COMMON_IMAGE_URL + url
        json_line['images']['thumbnail'] = PRODUCTION_IMAGE_URL + COMMON_IMAGE_URL + url
        json_line['images']['featured_image'] = PRODUCTION_IMAGE_URL + COMMON_IMAGE_URL + url
        json_line['images']['base_image'] = PRODUCTION_IMAGE_URL + COMMON_IMAGE_URL + url

        json_line['category_trees'][0]['id'] = primary_category + "/" + sub_category + "/" + leaf_category
        json_line['category_trees'][0]['label'] = primary_category + "/" + sub_category + "/" + leaf_category
        json_line['product_links'] = []
        json_line['currency'] = "USD"
        json_line['price'] = round(json_line['price'] * 0.014, 2)

        write_data(json_line)


def main():
    read_data()


if __name__ == "__main__":
    main()
