import argparse
import requests

from pathlib import Path

from fetch_images_helper import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="""Утилита для скачивания фото запусков SpaceX"""
    )
    parser.add_argument(
        "--launch_id",
        help="ID запуска SpaceX для скачивания фото"
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


def get_spacex_photos(launch_id, count):
    """Создает список ссылок на указанное число фото запуска SpaceX."""
    spacex_url = "https://api.spacexdata.com/v5/launches/"
    params = {
        "id": launch_id
    }
    response = requests.get(spacex_url, params=params)
    response.raise_for_status()
    data = response.json()
    if launch_id != "latest" and data[0]["id"] != launch_id:
        print(f"Вы указали неверный ID '{launch_id}'. Скачиваем фото последнего запуска...")
    result = []
    for item in data:
        if "links" in item and "flickr" in item["links"] and "original" in item["links"]["flickr"]:
            photos = item["links"]["flickr"]["original"]
            result.extend([photo for photo in photos if photo is not None])
    return result[:count]


def main():
    parser = create_parser()
    args = parser.parse_args()
    launch_id = args.launch_id if args.launch_id else "latest"
    count = int(args.count) if args.count else 10
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
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
