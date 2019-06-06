#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""

"""

import json


def write_data(json_data):
    with open('mobile_data.json', 'a') as f:
        f.write(json.dumps(json_data) + '\n')


def convert_to_usd(price):
        return price*0.014


def runner():
    item_id = 517
    while True:
        true = True
        title = input('name: ')
        small_image = input('small image: ')
        price = input('price: ')
        brand = input('brand: ')
        primary_category = 'Electronics'
        sub_category = 'Mobiles'
        leaf_category = input('leaf_category: ')
        category_tree = "{}/{}/{}".format(
                primary_category,
                sub_category,
                leaf_category
        )

        data_to_write = {
                "item_id": str(item_id),
                "title": title,
                "images": {
                        "small_image": small_image,
                        "thumbnail": small_image,
                        "featured_image": small_image,
                        "base_image": small_image
                },
                "brand": brand,
                "manufacturer": brand,
                "category_trees": [
                        {
                                "label": category_tree,
                                "is_primary": true,
                                "id": category_tree
                        }
                ],
                "item_type": "parent",
                "parent_id": 0,
                "visibility": {
                        "visible_in_catalog": true,
                        "visible_in_search": true
                },
                "in_stock": 1,
                "product_links": [],
                "product_attributes": [],
                "accessories": {},
                "features": {},
                "product_services": {},
                "reviews": [],
                "associated_item_ids": [],
                "tags": [],
                "sku": "",
                "classification": "",
                "rating": "",
                "price": convert_to_usd(price),
                "currency": "USD",
                "long_description": title,
                "short_description": title
        }

        write_data(data_to_write)

        item_id = item_id + 1


if __name__ == "__main__":
    runner()