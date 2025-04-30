import argparse
import requests

from pathlib import Path

from fetch_images_helper import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description='''Утилита для скачивания фото запусков SpaceX'''
    )
    parser.add_argument(
        '--launch_id',
        help='ID запуска SpaceX для скачивания фото'
    )
    return parser


def get_spacex_photos(launch_id):
    """Создает список ссылок на 10 фото указанного запуска SpaceX."""
    spacex_url = 'https://api.spacexdata.com/v5/launches/'
    params = {
        'id': launch_id
    }
    response = requests.get(spacex_url, params=params)
    response.raise_for_status()  # Проверка на ошибки HTTP
    data = response.json()
    if launch_id != 'latest' and data[0]['id'] != launch_id:
        print(f"Вы указали неверный ID '{launch_id}'. Скачиваем фото последнего запуска...")
    result = []
    for item in data:
        if 'links' in item and 'flickr' in item['links'] and 'original' in item['links']['flickr']:
            photos = item['links']['flickr']['original']
            result.extend([photo for photo in photos if photo is not None])
    return result[:10]


def main():
    parser = create_parser()
    args = parser.parse_args()
    launch_id = args.launch_id if args.launch_id else 'latest'
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    try:
        spacex_photos = get_spacex_photos(launch_id)
        if spacex_photos:
            fetch_photos(spacex_photos, images_dir, 'spacex')
            print('Фото от SpaceX сохранены!')
        else:
            print(f'Не удалось получить фотографии для запуска с ID: {launch_id}')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")


if __name__ == '__main__':
    main()
