import requests

from decouple import config
from pathlib import Path

from fetch_images_helper import fetch_photos


def get_apod_photos(nasa_token):
    """Создает список ссылок на 15 случайных фото NASA APOD."""
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_token,
        "count": "15"
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
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    nasa_token = config("NASA_TOKEN")
    apod_photos = get_apod_photos(nasa_token)
    fetch_photos(apod_photos, images_dir, "apod")
    print("Фото от NASA APOD сохранены!")


if __name__ == "__main__":
    main()
