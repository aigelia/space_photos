import argparse
import requests

from decouple import config
from pathlib import Path

from download_utils import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="Утилита для скачивания фото NASA APOD"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Количество фото для скачивания"
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default="images",
        help="Директория для сохранения изображений"
    )
    return parser


def fetch_apod_data(nasa_token, count):
    """Отправляет запрос к API NASA APOD и возвращает JSON с данными о фото."""
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_token,
        "count": count
    }
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    return response.json()


def get_apod_photos(data):
    """Извлекает список ссылок на изображения (исключая видео)."""
    result = []
    for item in data:
        if item.get("media_type") == "image":
            result.append(item["url"])
    return result


def main():
    parser = create_parser()
    args = parser.parse_args()
    count = args.count
    images_dir = args.folder
    images_dir.mkdir(exist_ok=True)
    nasa_token = config("NASA_TOKEN")
    data = fetch_apod_data(nasa_token, count)
    apod_photos = get_apod_photos(data)
    fetch_photos(apod_photos, images_dir, "apod")
    print("Фото от NASA APOD сохранены!")


if __name__ == "__main__":
    main()
