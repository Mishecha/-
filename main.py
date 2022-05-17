from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
import asyncio
import telegram

import os.path
import os

import random
import requests

import time
import datetime


nasa_api_key = os.environ['NASA_API_KEY']
telegram_token = os.environ['TELEGRAM_TOKEN']  
telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
bot = telegram.Bot(telegram_token)


async def send_photo(random_dir, random_file):
    with open(f'{random_dir}/{random_file}', 'rb') as file:
        bot.send_photo(chat_id=telegram_chat_id, photo=file)

      
def download_image(url, name, params1=''):
    response = requests.get(url, params=params1)
    response.raise_for_status()
    with open(name, 'wb') as file:
        file.write(response.content)


def create_folders_for_pictures():
    space_pictures_folders = ["image_nasa", "image_spacex", "image_nasa_epic"]
    for folder in space_pictures_folders:
        Path(folder).mkdir(parents=True, exist_ok=True)


def get_extension(user_link):
    parsed_link = urlparse(user_link)
    path = parsed_link.path
    splitext = os.path.splitext(path)
    return splitext[1]


def get_nasa_epic(nasa_api_key):
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

    download_image(nasa_epic_url, f'{nasa_epic_image_dir}/{number}{nasa_epic_file_name}', nasa_epic_params)


def get_nasa(nasa_api_key, nasa_image_dir):
    file_name_nasa = 'image_nasa'
    params_nasa = {'count': 50, 'api_key': nasa_api_key}
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(nasa_url, params=params_nasa)
    response.raise_for_status()
    
    for number, image in enumerate(response.json()):
        path_image_nasa = f'{nasa_image_dir}/{number}{file_name_nasa}{get_extension(image["url"])}'
        return download_image(nasa_url, path_image_nasa, params_nasa)


def get_spacex(spacex_image_dir):
    spacex_last_launch = 66
    spacex_file_name = 'image_SpaceX'
    spacex_url = 'https://api.spacexdata.com/v4/launches'

    response = requests.get(spacex_url)
    response.raise_for_status()

    spacex_link = response.json(
    )[spacex_last_launch]['links']['flickr']['original']

    for number, image in enumerate(spacex_link):
        response = requests.get(image)
        response.raise_for_status()

        download_image(spacex_url, f'{spacex_image_dir}/{number}{spacex_file_name}{get_extension(image)}')


if __name__ == "__main__":
    create_folders_for_pictures()
    load_dotenv()

    delay = 1
    nasa_epic_image_dir = 'image_nasa_epic'
    nasa_image_dir = 'image_nasa'
    spacex_image_dir = 'image_spacex'
  
    names_dir = [nasa_epic_image_dir, spacex_image_dir, nasa_image_dir]
    random_dir = random.choice(names_dir)
    random_file = random.choice(os.listdir(random_dir))
  
    while True:
        get_nasa(nasa_api_key)
        get_spacex(spacex_image_dir)
        get_nasa_epic(nasa_api_key)
        asyncio.run(send_photo(random_dir, random_file))
        time.sleep(delay)
          
