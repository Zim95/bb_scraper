import json

file_list = [
    'miami_data/men_sunglasses.csv',
    'miami_data/men_beach_shoes.csv',
    'miami_data/women_sunglasses.csv',
    'miami_data/women_beach_shoes.csv'
]


def main():
    item_id = 3908
    for item in file_list:
        with open(item, 'r') as f:
            lines = list(map(lambda x: x.strip(), f.readlines()))
        
        if item == file_list[0]:
            primary_category = 'men'
            secondary_category = 'mens-clothing'
            leaf_category = 'sunglasses'
        elif item == file_list[1]:
            primary_category = 'men'
            secondary_category = 'mens-clothing'
            leaf_category = 'miami-shoes'
        elif item == file_list[2]:
            primary_category = 'women'
            secondary_category = 'womens-clothing'
            leaf_category = 'sunglasses'
        elif item == file_list[3]:
            primary_category = 'women'
            secondary_category = 'womens-clothing'
            leaf_category = 'miami-shoes'
        for line in lines:
            title = line.split(",")[0]
            price = float(line.split(",")[1].strip())
            small_image = line.split(",")[2]
            brand = 'miami'
            
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
            item_id = item_id + 1
            with open('miami_accessories_apparel_data.json', 'a') as f:
                f.write(json.dumps(item_dict) + "\n")


if __name__ == "__main__":
    main()