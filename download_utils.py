import requests
from os.path import splitext
from urllib.parse import urlsplit


def check_file_extension(url):
    """Проверяет расширение изображений NASA/APOD/EPIC API."""
    path = urlsplit(url)[2]
    extension = splitext(path)[1]
    return extension


def download_photo(url, filepath):
    """Скачивает одно фото и сохраняет его в указанный путь."""
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, "wb") as file:
        file.write(response.content)


def fetch_photos(photo_links, images_dir, subdir_name):
    """Скачивает фото по ссылкам из списка, полученного от API."""
    subdir = images_dir / subdir_name
    subdir.mkdir(exist_ok=True)
    for photo_id, url in enumerate(photo_links):
        extension = check_file_extension(url)
        filename = f"{subdir_name}_{photo_id}{extension}"
        filepath = subdir / filename
        download_photo(url, filepath)
