import argparse
import requests

from decouple import config
from pathlib import Path

from fetch_images_helper import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="""Утилита для скачивания фото NASA APOD"""
    )
    parser.add_argument(
        "--count",
        help="Количество фото для скачивания"
    )
    parser.add_argument(
        "--folder",
        help="Директория для сохранения изображений"
    )
    return parser

def get_apod_photos(nasa_token, count):
    """Создает список ссылок на указанное количество случайных фото NASA APOD."""
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_token,
        "count": count
    }
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    data = response.json()
    result = []
    for item in data:
        photo = item["url"]
        result.append(photo)
    return result


def main():
    parser = create_parser()
    args = parser.parse_args()
    count = args.count if args.count else "10"
    images_dir = Path(args.folder) if args.folder else Path("images")
    images_dir.mkdir(exist_ok=True)
    nasa_token = config("NASA_TOKEN")
    apod_photos = get_apod_photos(nasa_token, count)
    fetch_photos(apod_photos, images_dir, "apod")
    print("Фото от NASA APOD сохранены!")


if __name__ == "__main__":
    main()
