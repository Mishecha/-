from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

import os.path
import os

import telegram
import random
import requests

import time
import datetime


def create_folders_for_pictures():
    Path("image_nasa").mkdir(parents=True, exist_ok=True)
    Path("image_SpaceX").mkdir(parents=True, exist_ok=True)
    Path("image_nasa_epic").mkdir(parents=True, exist_ok=True)


def get_extension(user_link):
    parsed_link = urlparse(user_link)
    path = parsed_link.path
    splitext = os.path.splitext(path)
    return splitext[1]


def get_nasa_epic(nasa_api_key):
    nasa_epic_params = {
        'api_key': nasa_api_key
    }
    nasa_epic_file_name = 'image_nasa_epic.png'
    nasa_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(nasa_epic_url, params=nasa_epic_params)
    response.raise_for_status()

    nasa_epic_pictures = response.json()[:number_images]
    for number, image in enumerate(nasa_epic_pictures):
        nasa_epic_image = image['image']
        nasa_epic_date = image['date']

        obj_date_time = datetime.datetime.strptime(nasa_epic_date, '%Y-%m-%d  %H:%M:%S')
        format_date = obj_date_time.strftime('%Y/%m/%d')

        nasa_epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{format_date}/png/{nasa_epic_image}.png'

        response = requests.get(nasa_epic_url, params=nasa_epic_params)
        response.raise_for_status()

        with open(f'{nasa_epic_image_dir}/{number}{nasa_epic_file_name}', 'wb') as file:
            file.write(response.content)


def get_nasa(nasa_api_key):
    file_name_nasa = 'image_nasa'
    params_nasa = {
        'count': 30,
        'api_key': nasa_api_key
    }
    url_nasa = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url_nasa, params=params_nasa)
    response.raise_for_status()

    for number, image in enumerate(response.json()):
        response = requests.get(image['url'])
        response.raise_for_status()

        with open(f'{nasa_image_dir}/{number}{file_name_nasa}{get_extension(image["url"])}', 'wb') as file:
            file.write(response.content)


def get_SpaceX():
    spacex_file_name = 'image_SpaceX.jpeg'
    url_spacex = 'https://api.spacexdata.com/v4/launches'

    response = requests.get(url_spacex)
    response.raise_for_status()

    spacex_link = response.json()[spacex_last_launch]['links']['flickr']['original']

    for number, image in enumerate(spacex_link):
        response = requests.get(image)
        response.raise_for_status()

        with open(f'{spacex_image_dir}/{number}{spacex_file_name}', 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    create_folders_for_pictures()

    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    delay = os.environ['DELAY']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    nasa_epic_image_dir = 'image_nasa_epic'
    nasa_image_dir = 'image_nasa'
    spacex_image_dir = 'image_SpaceX'

    spacex_last_launch = 66
    number_images = 9

    name_dir = [nasa_epic_image_dir, spacex_image_dir, nasa_image_dir]
    bot = telegram.Bot(token=telegram_token)
    while True:
        get_nasa()
        get_SpaceX()
        get_nasa_epic()
        random_dir = random.choice(name_dir)
        random_file = random.choice(os.listdir(random_dir))
        with open(f'{random_dir}/{random_file}', 'rb') as file:
            bot.send_document(chat_id=telegram_chat_id, document=file)

        time.sleep(delay)
