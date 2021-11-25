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


def get_nasa_epic():
    params_nasa_epic = {
        'api_key': api_key
    }
    file_name_nasa_epic = 'image_nasa_epic.png'
    url_nasa_epic = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(url_nasa_epic, params=params_nasa_epic)
    response.raise_for_status()

    lists_nasa_epic = response.json()[0:9]
    for number, image in enumerate(lists_nasa_epic):
        image_nasa_epic = image['image']
        date_nasa_epic = image['date']

        date_time_obj = datetime.datetime.strptime(date_nasa_epic, '%Y-%m-%d  %H:%M:%S')
        formatted_date = date_time_obj.strftime('%Y/%m/%d')

        url_nasa_epic = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/{image_nasa_epic}.png'

        response = requests.get(url_nasa_epic, params=params_nasa_epic)
        response.raise_for_status()

        with open(f'{image_dir_nasa_epic}/{number}{file_name_nasa_epic}', 'wb') as file:
            file.write(response.content)


def get_nasa():
    file_name_nasa = 'image_nasa'
    params_nasa = {
        'count': 30,
        'api_key': api_key
    }
    url_nasa = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url_nasa, params=params_nasa)
    response.raise_for_status()

    for number, image in enumerate(response.json()):
        response = requests.get(image['url'])
        response.raise_for_status()

        with open(f'{image_dir_nasa}/{number}{file_name_nasa}{get_extension(image["url"])}', 'wb') as file:
            file.write(response.content)


def get_SpaceX():
    file_name_SpaceX = 'image_SpaceX.jpeg'
    url_SpaceX = 'https://api.spacexdata.com/v4/launches'

    response = requests.get(url_SpaceX)
    response.raise_for_status()

    link_SpaceX = response.json()[66]['links']['flickr']['original']

    for number, image in enumerate(link_SpaceX):
        response = requests.get(image)
        response.raise_for_status()

        with open(f'{image_dir_SpaceX}/{number}{file_name_SpaceX}', 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    create_folders_for_pictures()

    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    delay = os.environ['DELAY']

    image_dir_nasa_epic = 'image_nasa_epic'
    image_dir_nasa = 'image_nasa'
    image_dir_SpaceX = 'image_SpaceX'


    name_dir = [image_dir_nasa_epic, image_dir_SpaceX, image_dir_nasa]
    bot = telegram.Bot(token=token)
    while True:
        get_nasa()
        get_SpaceX()
        get_nasa_epic()
        random_dir = random.choice(name_dir)
        random_file = random.choice(os.listdir(random_dir))
        bot.send_document(chat_id='@abc10101a', document=open(f'{random_dir}/{random_file}', 'rb'))
        time.sleep(delay)
