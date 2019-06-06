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
from pprint import pprint
import xlrd

def read_from_file():
    with open('../data/mobile_urls.json', 'r') as f:
        lines = f.readlines()
    return lines


def write_to_file(dictionary):
    with open('../data/miami_apparel_data.json', 'a') as f:
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
    item_id = 3831

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

def main():
    scrape()


if __name__ == "__main__":
    main()
