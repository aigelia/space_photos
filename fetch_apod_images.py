import argparse
import requests

from decouple import config
from pathlib import Path

from download_utils import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="Utility for downloading images from NASA APOD"
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


def fetch_apod_data(nasa_token, count):
    """Sends a request to the NASA APOD API and returns JSON data about the images."""
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_token,
        "count": count
    }
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    return response.json()


def get_apod_photos(data):
    """Extracts image URLs from the response (excluding videos)."""
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
    print("NASA APOD saved!")


if __name__ == "__main__":
    main()
