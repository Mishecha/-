import os.path
import os
from os import listdir
import time
import random

import telegram
from dotenv import load_dotenv


def get_random_path(names_directory):
    random_folder = random.choice(names_directory)
    random_file = random.choice(listdir(random_folder))
    random_path = f'{random_folder}/{random_file}'
    return random_path
    

if __name__ == "__main__":
    load_dotenv()

    nasa_epic_image_directory = os.environ['nasa_epic_image_directory']
    nasa_image_directory = os.environ['nasa_image_directory']
    spacex_image_directory = os.environ['spacex_image_directory']
    telegram_token = os.environ['TELEGRAM_TOKEN']  
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    delay = int(os.environ['DELAY'])
    
    bot = telegram.Bot(telegram_token)

    names_directory = [
        nasa_epic_image_directory,
        spacex_image_directory,
        nasa_image_directory
    ]
    
    while True:
        file_path = get_random_path(names_directory)
        with open(file_path, 'rb') as file:
            bot.send_photo(chat_id=telegram_chat_id, photo=file)
        time.sleep(delay)
