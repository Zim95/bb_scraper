# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: Test Scraper
Author: Namah
"""

from bs4 import BeautifulSoup
import requests
import re
import urllib3
import os
import argparse
import sys
import json

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search

used_image_names = []


def get_request(url, headers=None):
    http = urllib3.PoolManager()

    if headers is None:
        response = http.request('GET', url)
    else:
        response = http.request('GET', url, headers=headers)

    return response


def get_soup(url, header):
    response = get_request(url, headers=header)

    soup = BeautifulSoup(response.data)
    # return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')
    return soup


def get_all_movie_names():
    with open('../data/movie_names.txt', 'r') as f:
        names = f.readlines()
    return list(map(lambda x: x.strip(), names))


def check_used_image_names(image_name):
    if image_name in used_image_names:
        image_count = int(image_name[-1])
        image_count += 1
        image_name = image_name[:-1] + str(image_count)
        check_used_image_names(image_name)
    else:
        used_image_names.append(image_name)
    return image_name


def download_image(folder_name, image_url):
    image_name = check_used_image_names(
        folder_name.lower() + "0"
    )

    image_ext = image_url.split(".")[-1]

    image_data = requests.get(image_url).content

    try:
        with open('movie_images/' + folder_name +'/' + image_name + "." + image_ext, 'wb') as img_handler:
            img_handler.write(image_data)

        return folder_name + "/" + image_name+image_ext
    except Exception as e:
        print(e)
        return


def google_search(folder_name, url):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url, header)

    ActualImages = []  # contains the link for Large original images, type of image
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        ActualImages.append((link, Type))

    for item in ActualImages:
        download_image(folder_name, item[0])
    # for i, (img, Type) in enumerate(ActualImages[0:10]):
    #     try:
    #         img_data = requests.get(img).content
    #         try:
    #             with open('movie_images/' + img, 'wb') as img_handler:
    #                 img_handler.write(img_data)
    #         except Exception as e:
    #             print(e)
    #             continue
    #     except Exception as e:
    #         print("could not load : "+img)
    #         print(e)


def get_google_search_name(name):
    return "+".join(name.split(" "))


def get_folder_name(name):
    return "_".join(name.split(" "))


def make_folder(movie_name):
    folder_name = get_folder_name(movie_name)

    if not os.path.exists('movie_images/' + folder_name):
        os.makedirs('movie_images/' + folder_name)

    return folder_name


def get_url(query):
    url = 'https://www.google.co.in/search?q='+query+'&source=lnms&tbm=isch'
    return url


def run():
    all_movies = get_all_movie_names()
    for movie in all_movies:
        folder_name = make_folder(movie)
        query = get_google_search_name(movie + " movie poster")
        url = get_url(query)
        google_search(folder_name, url)

if __name__ == "__main__":
    run()