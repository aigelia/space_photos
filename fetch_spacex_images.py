import argparse
from pathlib import Path
import requests

from download_utils import fetch_photos


def create_parser():
    parser = argparse.ArgumentParser(
        description="Utility for downloading images from SpaceX launches"
    )
    parser.add_argument(
        "--launch_id",
        type=str,
        default="latest",
        help="SpaceX launch ID to download images from"
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default="images",
        help="Directory to save images"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of images to download (default is 10)"
    )
    return parser


def get_all_data(launch_id):
    """Sends a request to the SpaceX API and returns launch data in JSON."""
    url = "https://api.spacexdata.com/v5/launches/"
    params = {"id": launch_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_photo_urls(launch_data):
    """Extracts photo URLs from the launch data."""
    photo_urls = []
    for item in launch_data:
        links = item.get("links", {})
        flickr = links.get("flickr", {})
        originals = flickr.get("original", [])
        photo_urls.extend([url for url in originals if url])
    return photo_urls


def get_spacex_photos(launch_id, count):
    """Returns a list of photo URLs for the given SpaceX launch."""
    data = get_all_data(launch_id)
    if launch_id != "latest" and data[0]["id"] != launch_id:
        print(f"Invalid launch ID '{launch_id}'. Fetching images from the latest launch...")
    all_photos = get_photo_urls(data)
    return all_photos[:count]


def main():
    parser = create_parser()
    args = parser.parse_args()
    launch_id = args.launch_id
    count = args.count
    images_dir = args.folder
    images_dir.mkdir(parents=True, exist_ok=True)
    try:
        spacex_photos = get_spacex_photos(launch_id, count)
        if spacex_photos:
            fetch_photos(spacex_photos, images_dir, "spacex")
            print("SpaceX images saved!")
        else:
            print(f"No images found for launch ID: {launch_id}")
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
