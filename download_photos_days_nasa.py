import urllib.parse
import os.path
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from download_image import download_image


def get_extension(user_link):
    user_quote_link = urllib.parse.unquote(user_link,
                                           encoding='utf-8', errors='replace')
    parsed_link = urlparse(user_quote_link)
    path = parsed_link.path
    splitext = os.path.splitext(path)
    file_name, expansion = splitext
    return expansion


def download_photos_days_nasa(nasa_api_key,
                              nasa_image_directory, number_of_nasa_images=30):
    file_name_nasa = 'image_nasa'
    params_nasa = {'count': number_of_nasa_images, 'api_key': nasa_api_key}
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(nasa_url, params=params_nasa)
    response.raise_for_status()

    for number, image in enumerate(response.json()):
        if image["url"]:
            link_image_nasa = image["url"]
            extension_image_nasa = get_extension(link_image_nasa)
            path_image_nasa = (f'{nasa_image_directory}/{number}'
                               f'{file_name_nasa}{extension_image_nasa}')
            if extension_image_nasa == '.jpg' or '.gif':
                download_image(link_image_nasa, path_image_nasa, params_nasa)


def main():
    load_dotenv()
    space_image_directory = 'space_image'
    Path(space_image_directory).mkdir(parents=True, exist_ok=True)
    nasa_api_key = os.environ['NASA_API_KEY']

    download_photos_days_nasa(nasa_api_key, space_image_directory)

if __name__ == "__main__":
    main()
