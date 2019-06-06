import redis

MEDIASENSE_CONFIG = {
    "erosnow": {
        "root_genres": {
            "root_genre_main_div": {
                "xpath": '//*[@id="genreList"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "root_genre_link_root": {
                "xpath": './/div',
                "wait": False,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": None,
                "single": False
            },
            "root_genre_link": {
                "xpath": ".//a",
                "wait": False,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": 'href',
                "single": True
            },
            "root_genre_image": {
                "xpath": ".//a/img",
                "wait": False,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": 'src',
                "single": True
            },
            "root_genre_name": {
                "xpath": ".//a/img",
                "wait": False,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": 'alt',
                "single": True
            }
        },
        "genre_page": {
            "genre_page_main_div": {
                "xpath": '//*[@id="results"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "genre_page_link_root": {
                "xpath": ".//div",
                "wait": False,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": None,
                "single": False
            },
            "genre_page_link": {
                "xpath": ".//a",
                "wait": False,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": 'href',
                "single": True
            }
        },
        "product_page": {
            "product_page_title": {
                "xpath": '//*[@id="videoTitle"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": 'text',
                "single": True
            },
            "product_page_image": {
                "xpath": '//*[@id="videoBG"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": 'style',
                "single": True
            },
            "product_page_release_date": {
                "xpath": "/html/body/div[3]/div[4]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]/span[1]/a",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": 'text',
                "single": True
            },
            "product_page_duration": {
                "xpath": '//*[@id="videoData2"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": 'text',
                "single": True
            },
            "product_page_rating": {
                "xpath": "/html/body/div[3]/div[4]/div[2]/div[3]/div[1]/div[1]/div[3]/div[3]/div[5]/div[1]/span/span[2]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": 'class',
                "single": True
            },
            "product_page_description_root": {
                "xpath": '//*[@id="videoDescription"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_description": {
                "xpath": ".//div",
                "wait": True,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": 'text',
                "single": True
            },
            "product_page_extra_info_root": {
                "xpath": '//*[@id="extraInfo"]',
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_cast_root": {
                "xpath": ".//div[1]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_cast_links": {
                "xpath": ".//span/a",
                "wait": True,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": None,
                "single": False
            },
            "product_page_director_root": {
                "xpath": ".//div[2]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_director_links": {
                "xpath": ".//span/a",
                "wait": True,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": None,
                "single": False
            },
            "product_page_music_root": {
                "xpath": ".//div[3]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_music_links": {
                "xpath": ".//span/a",
                "wait": True,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": None,
                "single": False
            },
            "product_page_language_root": {
                "xpath": ".//div[4]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_language": {
                "xpath": ".//a",
                "wait": True,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": 'text',
                "single": True
            },
            "product_page_genre_root": {
                "xpath": ".//div[5]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "product_page_genre_links": {
                "xpath": ".//span/a",
                "wait": True,
                "wait_time": 10,
                "absolute": False,
                "target_attribute": None,
                "single": False
            },
            "product_page_hd": {
                "xpath": "/html/body/div[3]/div[4]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[1]/img",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": 'title',
                "single": True
            }
        }
    },
    "reuter": {
        "item_dictionary": {
            "title_tag": {
                "xpath": "", 
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": "text",
                "single": True
            },
            "image_tag": {
                "xpath": "",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": "",
                "single": True
            },
            "description_tag": {
                "xpath": "",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": "",
                "single": True
            },
            "published_at_tag": {
                "xpath": "",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": "",
                "single": True
            }
        },
        "get_urls": {
            "main_item_div": {
                "xpath": "/html/body/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]",
                "wait": True,
                "wait_time": 10,
                "absolute": True,
                "target_attribute": None,
                "single": True
            },
            "item_list": {
                "xpath": ".//div",
                "absolute": False,
                "parent": "main_item_div",
                "wait": False,
                "wait_time": 10,
                "target_attribute": None,
                "single": False
            },
            "item_source": {
                "xpath": ".//div/article/div[2]/div/a",
                "absolute": False,
                "parent": "item_list",
                "wait": False,
                "wait_time": 10,
                "target_attribute": None,
                "single": True
            }
        }
    }
}


REDIS_HOST = 'localhost'
REDIS_PORT = 6379

REDIS_POOL = redis.ConnectionPool(
    host=REDIS_HOST, port=REDIS_PORT)
REDIS_CLIENT = redis.StrictRedis(connection_pool=REDIS_POOL)
