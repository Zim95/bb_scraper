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

# for svg image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

DEFAULT_COUNT = 1
LOCALHOST_IMAGE_URL = 'http://localhost/repositories/Retailsense-Saas-dashboard/'
PRODUCTION_IMAGE_URL = 'https://retailsense.recosenselabs.com/'

COMMON_IMAGE_URL = 'retaildemo-views/retaildemo/static/assets/images/rsRetail/'

run_local = False
name = 'apparel'
subname = 'armani'

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
    if not os.path.exists(name + '_images/' + folder_name):
        os.makedirs(name + '_images/' + folder_name)

    try:
        with open(name + '_images/' + folder_name+'/'+image_name+image_ext, 'wb') as img_handler:
            img_handler.write(image_data)

        return folder_name + "/" + image_name+image_ext
    except Exception as e:
        print(e)
        return


def download_svg_image(folder_name=None, image_name=None, image_url=None):
    if image_url is None or image_url == 'None':
        return

    image_data = requests.get(image_url).content

    if folder_name is None:
        folder_name = 'default'
    image_ext = '.png'
    if image_name is None:
        image_name = 'default' + str(DEFAULT_COUNT) + image_ext
        DEFAULT_COUNT = DEFAULT_COUNT + 1
    if not os.path.exists('_images/' + folder_name):
        os.makedirs('_images/' + folder_name)

    try:
        drawing = svg2rlg(image_url)
        renderPM.drawToFile(drawing, name + '_images/' + folder_name+'/'+image_name+image_ext, fmt="PNG")
        # with open('mobile_images/' + folder_name+'/'+image_name+image_ext, 'wb') as img_handler:
        #     img_handler.write(image_data)

        return folder_name + "/" + image_name+image_ext
    except Exception as e:
        print(e)
        return


def remove_null(string):
    string_list = list(filter(lambda x: x not in ['', '-'], string.split('-')))
    return '-'.join(string_list)


def remove_special_characters_title(title):
    title = title.replace(',', '_')
    title = title.replace('&', '_')
    title = title.replace('(', '_')
    title = title.replace(')', '_')
    title = title.replace(' ', '_')
    return title


def parse_line(json_line):
    image_url = json_line['images']['small_image']

    label_string = json_line['category_trees'][0]['label']
    label_list = label_string.split("/")
    primary_category = label_list[0]
    sub_category = label_list[1]
    leaf_category = label_list[2]

    title = remove_special_characters_title(json_line['title'])
    return primary_category, sub_category, leaf_category, title, image_url


def replace_delimiter(delimiter, string):
    string_list = string.split(delimiter)
    return '_'.join(string_list)


def write_data_production(dictionary):
    with open(
        './production_{}_{}_data.json'.format(subname, name),
        'a'
    ) as f:
        f.write(json.dumps(dictionary) + "\n")


def write_data_local(dictionary):
    with open(
        './local_{}_{}_data.json'.format(subname, name),
        'a'
    ) as f:
        f.write(json.dumps(dictionary) + "\n")


def read_data():
    with open('./{}_{}_data.json'.format(subname, name), 'r') as f:
        lines = f.readlines()

    for line in lines:
        try:
            json_line = json.loads(line)
            primary_category, sub_category, leaf_category, title, img_url = parse_line(json_line)

            folder_name = primary_category + '/' + sub_category + '/' + leaf_category
            image_name = replace_delimiter('/', replace_delimiter(' ', title))
            img_extension = '.jpg'
            
            if img_extension == '.svg':
                url = download_svg_image(
                    folder_name=folder_name,
                    image_name=image_name,
                    image_url=img_url
                )
            else:
                url = download_image(
                    folder_name=folder_name,
                    image_name=image_name,
                    image_ext=img_extension,
                    image_url=img_url
                )
            
            if run_local is True:
                image_type = LOCALHOST_IMAGE_URL
            else:
                image_type = PRODUCTION_IMAGE_URL

            json_line['images']['small_image'] = image_type + COMMON_IMAGE_URL + url
            json_line['images']['thumbnail'] = image_type + COMMON_IMAGE_URL + url
            json_line['images']['featured_image'] = image_type + COMMON_IMAGE_URL + url
            json_line['images']['base_image'] = image_type + COMMON_IMAGE_URL + url
            json_line['category_trees'][0]['id'] = json_line['category_trees'][0]['label']

            if run_local is True:
                write_data_local(json_line)
            else:
                write_data_production(json_line)
        except Exception as e:
            print(e)
            continue


def main():
    read_data()


if __name__ == "__main__":
    main()
