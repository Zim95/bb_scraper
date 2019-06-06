import json
from datetime import datetime, timedelta
from dateutil import parser

client_id = 'ufwcotnmdnqx2jl2qpyf'


def get_lines():
    with open('erosnow_intermediatory_file_new.json', 'r') as f:
        return list(
            map(
                lambda x: json.loads(x.strip()),
                f.readlines()
            )
        )


def convert_data_format(line):
    title = line['title']
    image = line['image']
    item_id = image.split("/")[5]
    released_date = line['release_date']
    product_duration = line['product_duration']
    rating = line['rating'],
    description = line['description']
    available_quality = line['quality']
    cast = line['cast'],
    director = line['director']
    music = line['music']
    language = line['language']
    genre = line['genre']

    item_dictionary = {
        "item_id": item_id,
        "client_id": client_id,
        "title": title,
        "description": description,
        "category": [
            "movie"
        ],
        "item_type": "full movie",
        "language": language,
        "image": image,
        "genres": genre,
        "actor": cast,
        "director": director,
        "music": music,
        "published_date": released_date,
        "released_date": released_date,
        "state": "active",
        "schedule": {
            "starts_at": released_date,
            "ends_at": (parser.parse(released_date) + timedelta(6 * 365/12)).isoformat()
        },
        "extra": {
            "ratings": rating,
            "available_quality": available_quality,
            "duration": product_duration
        }
    }

    return item_dictionary


def write_to_file(filename, item_dictionary):
    filename = filename + ".json"
    with open(filename, 'a') as f:
        f.write(json.dumps(item_dictionary) + "\n")


def main():
    lines = get_lines()
    for line in lines:
        item_dictionary = convert_data_format(line)
        write_to_file('erosnow_final_data_new', item_dictionary)


if __name__ == "__main__":
    main()