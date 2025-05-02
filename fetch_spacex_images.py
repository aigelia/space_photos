import argparse
from pathlib import Path
import requests

from fetch_images_helper import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="Утилита для скачивания фото запусков SpaceX"
    )
    parser.add_argument(
        "--launch_id",
        help="ID запуска SpaceX для скачивания фото"
    )
    parser.add_argument(
        "--folder",
        help="Директория для сохранения изображений"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Количество фотографий для скачивания (по умолчанию 10)"
    )
    return parser


def get_all_data(launch_id):
    """Отправляет запрос к API SpaceX и возвращает JSON с данными о запуске."""
    url = "https://api.spacexdata.com/v5/launches/"
    params = {
        "id": launch_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_photo_urls(launch_data):
    """Получает нужные фото из данных о запусках."""
    photo_urls = []
    for item in launch_data:
        links = item.get("links", {})
        flickr = links.get("flickr", {})
        originals = flickr.get("original", [])
        photo_urls.extend([url for url in originals if url])
    return photo_urls


def get_spacex_photos(launch_id, count):
    """Создает список ссылок на указанное число фото запуска SpaceX."""
    data = get_all_data(launch_id)
    if launch_id != "latest" and data[0]["id"] != launch_id:
        print(f"Вы указали неверный ID '{launch_id}'. Скачиваем фото последнего запуска...")
    all_photos = get_photo_urls(data)
    return all_photos[:count]


def main():
    parser = create_parser()
    args = parser.parse_args()
    launch_id = args.launch_id or "latest"
    count = args.count
    images_dir = Path(args.folder) if args.folder else Path("images")
    images_dir.mkdir(parents=True, exist_ok=True)
    try:
        spacex_photos = get_spacex_photos(launch_id, count)
        if spacex_photos:
            fetch_photos(spacex_photos, images_dir, "spacex")
            print("Фото от SpaceX сохранены!")
        else:
            print(f"Не удалось получить фотографии для запуска с ID: {launch_id}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
