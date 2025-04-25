import requests
from datetime import datetime, timedelta
from urllib.parse import urlsplit
from os.path import splitext

from decouple import config
from pathlib import Path


def get_spacex_photos():
    """Создает список ссылок на 15 фото последнего запуска SpaceX."""
    spacex_url = 'https://api.spacexdata.com/v5/launches/'
    params = {
        'id': 'latest'
    }
    response = requests.get(spacex_url, params=params)
    response.raise_for_status()
    data = response.json()
    result = []
    for item in data:
        if 'links' in item and 'flickr' in item['links'] and 'original' in item['links']['flickr']:
            photos = item['links']['flickr']['original']
            result.extend([photo for photo in photos if photo is not None])
    return result[:10]


def fetch_spacex_last_launch(spacex_photos, images_dir):
    """Скачивает фото SpaceX по ссылкам из списка, полученного от API"""
    spacex_dir = images_dir / 'spacex'
    spacex_dir.mkdir(exist_ok=True)
    for photo_id, photo in enumerate(spacex_photos):
        response = requests.get(photo)
        response.raise_for_status()
        filepath = spacex_dir / f'spacex_{photo_id}.jpg'
        with open(filepath, 'wb') as file:
            file.write(response.content)
    print('Фото от SpaceX сохранены!')


def check_file_extension(url):
    """Проверяет расширение изображений NASA APOD API"""
    path = urlsplit(url)[2]
    extension = splitext(path)[1]
    return extension


def get_apod_photos(nasa_token):
    """Создает список ссылок на 15 случайных фото NASA APOD."""
    apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_token,
        'count': '15'
    }
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    data = response.json()
    result = []
    for item in data:
        photo = item['url']
        result.append(photo)
    return result


def fetch_apod_photos(apod_photos, images_dir):
    """Скачивает фото NASA APOD по ссылкам из списка, полученного от API"""
    apod_dir = images_dir / 'apod'
    apod_dir.mkdir(exist_ok=True)
    for photo_id, photo in enumerate(apod_photos):
        file_extension = check_file_extension(photo)
        response = requests.get(photo)
        response.raise_for_status()
        filepath = apod_dir / f'apod_{photo_id}{file_extension}'
        with open(filepath, 'wb') as file:
            file.write(response.content)
    print('Фото от NASA APOD сохранены!')


def get_epic_photos(nasa_token):
    """Создает список ссылок на 10 фото NASA EPIC."""
    yesterday = datetime.today() - timedelta(days=1)
    date = yesterday.strftime('%Y-%m-%d')
    epic_url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    params = {
        'api_key': nasa_token
    }
    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    data = response.json()
    result = []
    for item in data[:10]:  # Ограничиваем до 10 фото
        image_name = item['image']
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{date[:4]}/{date[5:7]}/{date[8:10]}/png/{image_name}.png?api_key={nasa_token}'
        result.append(image_url)
    return result


def fetch_epic_photos(epic_photos, images_dir):
    """Скачивает фото NASA EPIC по ссылкам из списка, полученного от API"""
    epic_dir = images_dir / 'epic'
    epic_dir.mkdir(exist_ok=True)
    for photo_id, photo in enumerate(epic_photos):
        response = requests.get(photo)
        response.raise_for_status()
        filepath = epic_dir / f'epic_{photo_id}.png'
        with open(filepath, 'wb') as file:
            file.write(response.content)
    print('Фото от NASA EPIC сохранены!')


def main():
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    nasa_token = config('NASA_TOKEN')
    spacex_photos = get_spacex_photos()
    fetch_spacex_last_launch(spacex_photos, images_dir)
    apod_photos = get_apod_photos(nasa_token)
    fetch_apod_photos(apod_photos, images_dir)
    epic_photos = get_epic_photos(nasa_token)
    fetch_epic_photos(epic_photos, images_dir)


if __name__ == '__main__':
    main()
