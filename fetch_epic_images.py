import argparse
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode

from decouple import config
from pathlib import Path

from download_utils import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="Утилита для скачивания фото NASA EPIC"
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


def get_epic_date():
    """Возвращает дату за 7 дней до текущей в формате YYYY-MM-DD."""
    week_ago = datetime.today() - timedelta(days=7)
    return week_ago.strftime("%Y-%m-%d")


def fetch_epic_data(date, nasa_token):
    """Делает запрос к NASA EPIC API и возвращает JSON-данные."""
    epic_url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
    params = {"api_key": nasa_token}
    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    return response.json()


def build_epic_image_urls(data, date, count, nasa_token):
    """Создаёт список ссылок на изображения по данным EPIC."""
    year, month, day = date.split("-")
    params = {"api_key": nasa_token}
    result = []
    for item in data[:count]:
        image_name = item.get("image")
        if not image_name:
            continue
        base_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
        image_url = f"{base_url}?{urlencode(params)}"
        result.append(image_url)
    return result


def main():
    parser = create_parser()
    args = parser.parse_args()
    count = int(args.count) if args.count else 10
    images_dir = Path(args.folder) if args.folder else Path("images")
    images_dir.mkdir(exist_ok=True)
    nasa_token = config("NASA_TOKEN")
    date = get_epic_date()
    data = fetch_epic_data(date, nasa_token)
    epic_photos = build_epic_image_urls(data, date, count, nasa_token)
    fetch_photos(epic_photos, images_dir, "epic")
    print("Фото от NASA EPIC сохранены!")


if __name__ == "__main__":
    main()
