import os.path
import os
import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_image import download_image


def download_photos_nasa_epic(nasa_api_key, nasa_epic_image_directory, number_images=9):
    nasa_epic_params = {'api_key': nasa_api_key}
    nasa_epic_file_name = 'image_nasa_epic.png'
    nasa_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(nasa_epic_url, params=nasa_epic_params)
    response.raise_for_status()
    nasa_epic_pictures = response.json()[:number_images]
    for number, image in enumerate(nasa_epic_pictures):
        nasa_epic_image = image['image']
        nasa_epic_date = image['date']

        time_date = datetime.datetime.strptime(nasa_epic_date, '%Y-%m-%d  %H:%M:%S')
        format_date = time_date.strftime('%Y/%m/%d')

        nasa_epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{format_date}/png/{nasa_epic_image}.png'

        download_image(nasa_epic_url, f'{nasa_epic_image_directory}/{number}{nasa_epic_file_name}', nasa_epic_params)


def main():
    load_dotenv()
    space_image_directory = os.environ['SPACE_IMAGE_DIRECTORY']
    Path(space_image_directory).mkdir(parents=True, exist_ok=True)
    nasa_api_key = os.environ['NASA_API_KEY']

    download_photos_nasa_epic(nasa_api_key, space_image_directory)

if __name__ == "__main__":
    main()
