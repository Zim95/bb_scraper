import requests
import json

run_local = True
filename = 'miami_apparel_printed_shorts'
wfilename = 'miami_apparel_printed_shorts_result'


def get_read_filename():
    if run_local:
        prefix = 'local_'
    else:
        prefix = 'production_'

    return prefix + filename + '.json'


def get_write_filename():
    if run_local:
        prefix = 'local_'
    else:
        prefix = 'production_'

    return prefix + wfilename + '.json'


def read_data():
    with open(get_read_filename(), 'r') as f:
        lines = f.readlines()

    return lines


def construct_data():
    lines = read_data()

    data = {
        'client_id': 'rs-retail',
        'items': [],
        'action': 'update'
    }

    for line in lines:
        data['items'].append(json.loads(line))

    return data


def main():
    data = construct_data()
    with open(get_write_filename(), 'a') as f:
        f.write(json.dumps(data))
    print("DONE")


if __name__ == "__main__":
    main()
