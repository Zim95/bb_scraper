import json
import csv
import random
import datetime
import codecs


def get_time():
    return datetime.datetime.utcnow()


def write_to_file(data):
    with open('furniture_data_Wayfair.json', 'a') as f:
        f.write(json.dumps(data) + "\n")


def csv_to_json():
    final_list = []
    # Change each fieldname to the appropriate field name. 
    reader = csv.DictReader(
        codecs.open('wafer2.csv', 'rU', 'utf-8'),
        fieldnames=(
            "id", "title", "type",
            "images", "overview"
            )
    )  

    # Parse the CSV into JSON  
    for row in reader:
        try:
            if row:
                final_list.append(json.dumps(row))
            else:
                continue
        except Exception as e:
            continue

    return final_list


def convert_furniture_data(data):
    item_id = 1738
    for item in data:
        item = json.loads(item)
        main_category = 'furniture'
        title = item.get('title')
        image = eval(item.get('images'))[0]
        sub_category = item.get(
            'type').lower().replace(
                ' ', '-').replace('&', '-').replace('---', '-')
        brand = 'wayfair'
        price = random.randint(50, 100)*10
        overview = item.get('overview')

        item_dict = {
            'item_id': str(item_id),
            'title': title,
            'images': {
                'small_image': image,
                'thumbnail': image,
                'featured_image': image,
            },
            'brand': brand,
            'manufacturer': '',
            'category_trees': [
                {
                    'label': '{}/{}'.format(
                        main_category,
                        sub_category
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
            "sku": '',
            "classification": "",
            "rating": "",
            "price": round(float(price - 1), 2),
            "currency": "USD",
            "long_description": overview,
            "short_description": overview
        }

        write_to_file(item_dict)
        print(item_dict)
        print('WRITTEN for id .... ' + str(item_id))
        item_id = item_id + 1


def main():
    data = csv_to_json()
    convert_furniture_data(data[1:])

if __name__ == "__main__":
    main()
