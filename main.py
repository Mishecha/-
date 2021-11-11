from pathlib import Path
import requests
from urllib.parse import urlparse
import os.path
from pprint import pprint
import datetime
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.environ['API_KEY']

image_dir_nasa_epic = 'image_nasa_epic'
image_dir_nasa = 'image_nasa'
image_dir_SpaceX = 'image_SpaceX'

file_name_nasa_epic = 'image_nasa_epic.png'
file_name_nasa = 'image_nasa'
file_name_SpaceX = 'image_SpaceX.jpeg'

url_nasa = 'https://api.nasa.gov/planetary/apod'
url_SpaceX = 'https://api.spacexdata.com/v4/launches'


params_nasa = {
    'count': 30,
    'api_key': api_key
}

params_nasa_epic = {
    'api_key': api_key
}


def downloading_images():
    Path("image_nasa").mkdir(parents=True, exist_ok=True)
    Path("image_SpaceX").mkdir(parents=True, exist_ok=True)
    Path("image_nasa_epic").mkdir(parents=True, exist_ok=True)


def get_expansion(user_link):
    parsed_link = urlparse(user_link)
    path = parsed_link.path
    splitext = os.path.splitext(path)
    return splitext[1]


def get_nasa_epic():
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
    response = requests.get(url_nasa, params=params_nasa)
    response.raise_for_status()

    for number, image in enumerate(response.json()):
        response = requests.get(image['url'])
        response.raise_for_status()

        with open(f'{image_dir_nasa}/{number}{file_name_nasa}{get_expansion(image["url"])}', 'wb') as file:
            file.write(response.content)


def get_SpaceX():
    response = requests.get(url_SpaceX)
    response.raise_for_status()
    link_SpaceX = response.json()[66]['links']['flickr_images']

    for number, image in enumerate(link_SpaceX):
        response = requests.get(image)
        response.raise_for_status()

        with open(f'{image_dir_SpaceX}/{number}{file_name_SpaceX}', 'wb') as file:
            file.write(response.content)


downloading_images()
get_nasa_epic()
get_SpaceX()
get_nasa()


#2132631430:AAFKMC8P7-rURZPvTMypAPSrUTDOPYIdxVg
