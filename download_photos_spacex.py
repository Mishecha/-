import os.path
import os
from pathlib import Path
import argparse

import requests
from dotenv import load_dotenv

from download_image import download_image


def download_photos_spacex(spacex_image_directory, spacex_last_launch):
    spacex_file_name = 'image_spacex'
    spacex_url = 'https://api.spacexdata.com/v4/launches'

    response = requests.get(spacex_url)
    response.raise_for_status()

    spacex_link = response.json(
    )[spacex_last_launch]['links']['flickr']['original']

    for number, image in enumerate(spacex_link):
        download_image(image, f'{spacex_image_directory}/{number}'
                       f'{spacex_file_name}.jpg')


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
      description='Номер запуска'
    )
    parser.add_argument('spacex_id', default=66, 
                        type=int, nargs='?')
    spacex_launch = parser.parse_args().spacex_id
    space_image_directory = os.getenv('SPACE_IMAGE_DIRECTORY', 
                                      default='space_image')
    Path(space_image_directory).mkdir(parents=True, exist_ok=True)
    download_photos_spacex(space_image_directory, spacex_launch)

if __name__ == "__main__":
    main()
