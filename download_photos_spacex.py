import urllib.parse
import os.path
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv



def download_image(url, file_path, params1=''):
    response = requests.get(url, params=params1)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def create_folders_for_pictures():
    space_pictures_folders = ['image_spacex']
    for folder in space_pictures_folders:
        Path(folder).mkdir(parents=True, exist_ok=True)


def get_extension(user_link):
    user_unquote_link = urllib.parse.unquote(user_link, encoding='utf-8', errors='replace')
    parsed_link = urlparse(user_unquote_link)
    path = parsed_link.path
    splitext = os.path.splitext(path)
    return splitext[1]
  
def download_photos_spacex(spacex_image_directory):
    spacex_last_launch = 66
    spacex_file_name = 'image_spacex'
    spacex_url = 'https://api.spacexdata.com/v4/launches'

    response = requests.get(spacex_url)
    response.raise_for_status()

    spacex_link = response.json(
    )[spacex_last_launch]['links']['flickr']['original']

    for number, image in enumerate(spacex_link):
        download_image(image, f'{spacex_image_directory}/{number}{spacex_file_name}.jpg')


def main():
    load_dotenv()    
    spacex_image_directory = os.environ['spacex_image_directory']
  
    create_folders_for_pictures()
    download_photos_spacex(spacex_image_directory)

if __name__ == "__main__":
    main()


