import os.path
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_image import download_image

  
def download_photos_spacex(spacex_image_directory, spacex_last_launch=66):
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
    Path('image_spacex').mkdir(parents=True, exist_ok=True)
    spacex_image_directory = os.environ['SPACEX_IMAGE_DIRECTORY']

    download_photos_spacex(spacex_image_directory)

if __name__ == "__main__":
    main()
