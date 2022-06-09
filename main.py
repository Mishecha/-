import asyncio
import os.path
import os
import random
import time

import telegram
from dotenv import load_dotenv

nasa_epic_image_directory = os.environ['nasa_epic_image_directory']
nasa_image_directory = os.environ['nasa_image_directory']
spacex_image_directory = os.environ['spacex_image_directory']
telegram_token = os.environ['TELEGRAM_TOKEN']  
telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
delay = int(os.environ['DELAY'])
bot = telegram.Bot(telegram_token)

def get_file_path(names_directory):
    name_directory = random.choice(names_directory)
    name_image = random.choice(os.listdir(name_directory))
    file_path = f'{name_directory}/{name_image}'
    return file_path


async def send_photo(file_path):
    with open(file_path, 'rb') as file:
        bot.send_photo(chat_id=telegram_chat_id, photo=file)


if __name__ == "__main__":
    load_dotenv()
  
    names_directory = [
                    nasa_epic_image_directory, 
                    spacex_image_directory, 
                    nasa_image_directory
    ]

    file_path = get_file_path(names_directory)
  
    while True:
        asyncio.run(send_photo(file_path))
        time.sleep(delay)
