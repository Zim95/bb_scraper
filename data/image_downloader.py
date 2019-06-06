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

Base_img_folder = '/var/www/RetailSense-Saas-dashboard/retaildemo-views/retaildemo/static/assets/images/rsRetail/'


def download_image(folder_name=None, image_name=None , image_url=None):
    if image_url is None or image_url == 'None':
        return

    image_data = requests.get(image_url).content

    if folder_name is None:
        folder_name = 'default'

    with open(Base_img_folder+folder_name+'/'+image_name):
        pass


def remove_null(string):
    string_list = list(filter(lambda x: x != '', string.split('-')))
    return '-'.join(string_list)

def parse_line(line):
    json_line = json.loads(line)
    image_url = json_line['images']['small_image']
    label = json_line['category_trees'][0]['label']
    label.replace('')


def read_data():
    with open('./backup_all_data.json', 'r') as f:
        lines = file.readlines()

    for line in lines:
        image_name, image_url, folder_name = parse_line(line)