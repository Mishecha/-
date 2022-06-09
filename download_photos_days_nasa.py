import urllib.parse
import os.path
import os
import datetime
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
    space_pictures_folders = ["image_nasa", "image_nasa_epic"]
    for folder in space_pictures_folders:
        Path(folder).mkdir(parents=True, exist_ok=True)


def get_extension(user_link):
    user_unquote_link = urllib.parse.unquote(user_link, encoding='utf-8', errors='replace')
    parsed_link = urlparse(user_unquote_link)
    path = parsed_link.path
    splitext = os.path.splitext(path)
    return splitext[1]
  

def download_photos_nasa_epic(nasa_api_key, nasa_epic_image_directory):
    number_images = 9
    nasa_epic_params = {'api_key': nasa_api_key}
    nasa_epic_file_name = 'image_nasa_epic.png'
    nasa_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(nasa_epic_url, params=nasa_epic_params)
    response.raise_for_status()
    nasa_epic_pictures = response.json()[:number_images]
    for number, image in enumerate(nasa_epic_pictures):
        nasa_epic_image = image['image']
        nasa_epic_date = image['date']

        timen = datetime.datetime.strptime(nasa_epic_date, '%Y-%m-%d  %H:%M:%S')
        format_date = timen.strftime('%Y/%m/%d')

        nasa_epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{format_date}/png/{nasa_epic_image}.png'

        download_image(nasa_epic_url, f'{nasa_epic_image_directory}/{number}{nasa_epic_file_name}', nasa_epic_params)


def download_photos_days_nasa(nasa_api_key, nasa_image_directory):
    number_of_nasa_images = 30
    file_name_nasa = 'image_nasa'
    params_nasa = {'count': number_of_nasa_images, 'api_key': nasa_api_key}
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(nasa_url, params=params_nasa)
    response.raise_for_status()
    
    for number, image in enumerate(response.json()):
        if image["url"]:
            link_image_nasa = image["url"]
            expansion_image_nasa = get_extension(link_image_nasa)
            path_image_nasa = f'{nasa_image_directory}/{number}{file_name_nasa}{expansion_image_nasa}'
            if expansion_image_nasa == '.jpg' or '.gif':
                download_image(link_image_nasa, path_image_nasa, params_nasa)

def main():
    load_dotenv()
    nasa_epic_image_directory = os.environ['nasa_epic_image_directory']
    nasa_image_directory = os.environ['nasa_image_directory']
    nasa_api_key = os.environ['NASA_API_KEY']
  
    create_folders_for_pictures()
    download_photos_days_nasa(nasa_api_key, nasa_image_directory)
    download_photos_nasa_epic(nasa_api_key, nasa_epic_image_directory)

if __name__ == "__main__":
    main()
