import requests

def download_image(url, file_path, params1=''):
    response = requests.get(url, params=params1)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
