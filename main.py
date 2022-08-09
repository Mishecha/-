import os.path
import os
from os import listdir
import time
import random

import telegram
from dotenv import load_dotenv


def get_random_path(name_directory):
    random_file = random.choice(listdir(name_directory))
    random_path = f'{name_directory}/{random_file}'
    return random_path
    

if __name__ == "__main__":
    load_dotenv()

    space_image_directory = 'space_image'
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    delay = int(os.environ['DELAY'])
    
    bot = telegram.Bot(telegram_token)

    try:
        while True:
            file_path = get_random_path(space_image_directory)
            with open(file_path, 'rb') as file:
                bot.send_photo(chat_id=telegram_chat_id, photo=file)
            time.sleep(delay)
    except telegram.error.NetworkError:
        time.sleep(25)
