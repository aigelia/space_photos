import requests
from os.path import splitext

from urllib.parse import urlsplit


def check_file_extension(url):
    """Проверяет расширение изображений NASA APOD API"""
    path = urlsplit(url)[2]
    extension = splitext(path)[1]
    return extension


def fetch_photos(photo_links, images_dir, subdir_name):
    """Скачивает фото по ссылкам из списка, полученного от API."""
    subdir = images_dir / subdir_name
    subdir.mkdir(exist_ok=True)
    for photo_id, photo in enumerate(photo_links):
        file_extension = check_file_extension(photo)
        response = requests.get(photo)
        response.raise_for_status()
        filepath = subdir / f'{subdir_name}_{photo_id}{file_extension}'
        with open(filepath, 'wb') as file:
            file.write(response.content)