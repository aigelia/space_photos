from datetime import datetime, timedelta
import requests

from decouple import config
from pathlib import Path

from fetch_images_helper import fetch_photos


def get_epic_photos(nasa_token):
    """Создает список ссылок на 10 фото NASA EPIC."""
    week_ago = datetime.today() - timedelta(days=7)
    date = week_ago.strftime('%Y-%m-%d')
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


def main():
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    nasa_token = config('NASA_TOKEN')
    epic_photos = get_epic_photos(nasa_token)
    fetch_photos(epic_photos, images_dir, 'epic')
    print('Фото от NASA EPIC сохранены!')


if __name__ == '__main__':
    main()
