import xlrd
import os
import json

file_list = ['miami_data/women_miami_tops.xlsx', 'miami_data/women_floral_dresses.xlsx', 'miami_data/women_jumpsuits.xlsx'] 


def main():
    item_id = 3805
    for item in file_list:
        # Give the location of the file 
        price_list = []
        image_list = []
        title_list = []
        loc = (item)  
    
        # To open Workbook  
        wb = xlrd.open_workbook(loc)  
        sheet = wb.sheet_by_index(0) 
        
        row_count = 20 
        
        if item == 'miami_data/women_miami_tops.xlsx': 
            columns = [1, 3, 4] 
        elif item == 'miami_data/women_floral_dresses.xlsx': 
            columns = [1, 2, 3] 
        else: 
            columns = [1, 2, 3] 

        for i in range(0, row_count + 1):
            for j in columns: 
                cell_value = sheet.cell_value(i,j) 
                if j == 1: 
                    image_list.append(cell_value) 
                elif item != 'miami_data/women_miami_tops.xlsx' and j == 2: 
                    title_list.append(cell_value) 
                elif item == 'miami_data/women_miami_tops.xlsx' and j == 3: 
                    title_list.append(cell_value) 
                elif item != 'miami_data/women_miami_tops.xlsx' and j == 3: 
                    if item != 'miami_data/women_miami_tops.xlsx': 
                        if '$' not in cell_value: 
                            cell_value = sheet.cell_value(i, 5).split(" ")[-1] 
                    price_list.append(cell_value) 
                elif item == 'miami_data/women_miami_tops.xlsx' and j == 4: 
                    price_list.append(cell_value) 
    
        for i in range(0, len(image_list)):
            title = title_list[i]
            small_image = image_list[i]
            price = float(price_list[i].replace('$', ''))
            primary_category = 'women'
            secondary_category = 'womens-clothing'
            if item == 'miami_data/women_miami_tops.xlsx': 
                leaf_category = 'miami-tops' 
            elif item == 'miami_data/women_floral_dresses.xlsx': 
                leaf_category = 'floral-dresses'
            else: 
                leaf_category = 'jumpsuits'
            brand = 'Miami'
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

            with open('miami_apparel_data.json', 'a') as f:
                f.write(json.dumps(item_dict) + "\n")
            item_id = item_id + 1

if __name__ == "__main__":
    main()