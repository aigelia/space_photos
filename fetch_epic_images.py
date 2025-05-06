import argparse
from datetime import datetime, timedelta
import requests
from requests.models import PreparedRequest

from decouple import config
from pathlib import Path

from download_utils import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="Utility for downloading images from NASA EPIC"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of images to download"
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default="images",
        help="Directory to save images"
    )
    return parser


def get_epic_date():
    """Returns the date 7 days ago in YYYY-MM-DD format."""
    week_ago = datetime.today() - timedelta(days=7)
    return week_ago.strftime("%Y-%m-%d")


def fetch_epic_data(date_str, nasa_token):
    """Sends a request to NASA EPIC API and returns JSON data."""
    epic_url = f"https://api.nasa.gov/EPIC/api/natural/date/{date_str}"
    params = {"api_key": nasa_token}
    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    return response.json()


def build_epic_image_urls(data, date_str, count, nasa_token):
    """Builds a list of image URLs from EPIC API data."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    params = {"api_key": nasa_token}
    result = []

    for item in data[:count]:
        image_name = item.get("image")
        if not image_name:
            continue

        base_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{date.year}/{date.month:02}/{date.day:02}/png/{image_name}.png"
        )

        prepared = PreparedRequest()
        prepared.prepare_url(base_url, params)
        image_url = prepared.url

        result.append(image_url)

    return result


def main():
    parser = create_parser()
    args = parser.parse_args()
    count = args.count
    images_dir = args.folder
    images_dir.mkdir(exist_ok=True)
    nasa_token = config("NASA_TOKEN")
    date_str = get_epic_date()
    data = fetch_epic_data(date_str, nasa_token)
    epic_photos = build_epic_image_urls(data, date_str, count, nasa_token)
    fetch_photos(epic_photos, images_dir, "epic")
    print("NASA EPIC images saved!")


if __name__ == "__main__":
    main()
