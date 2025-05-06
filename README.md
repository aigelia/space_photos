# Just Space: Download NASA and SpaceX Photos and Publish Them to Telegram # 

**Just Space** is a collection of scripts that automate the downloading of photos from NASA and SpaceX, as well as publishing them to Telegram channels. Each script can be used independently. Here's how it works.

## Installation ##

You'll need Python 3.10 or lower (e.g., 3.9). The scripts are not guaranteed to work with Python 3.11+. To install required libraries, run:

```bash
pip install -r requirements.txt
```

Then, create a `.env` file in the root project directory and add the following keys:

1. `NASA_TOKEN=...` – your NASA API key, which can be obtained [here](https://api.nasa.gov) (no registration required).
2. `TG_TOKEN=...` – your Telegram bot token, which you can generate using [BotFather](https://telegram.me/BotFather).
3. `TG_CHAT_ID=...` – your Telegram channel ID (usually looks like `@yourchannelname`).

## Automatic Photo Posting

### `post_on_telegram.py` ###

This script publishes photos from any subdirectory inside the `images` directory. You can manually add images to this directory or use one of the fetching scripts below to populate it automatically.

**Important:** Make sure your Telegram bot is added to the channel and has admin permissions before running the script.

Photos will be posted in a loop. Once all images have been published, the script will reshuffle and start over. By default, it posts every 4 hours. You can change this interval using the `--sleeptime` argument (in seconds). For example, to post every hour:

```bash
python3 post_on_telegram.py --sleeptime 3600
```

Также можно указать, откуда брать изображения, с помощью аргумента `--directory`. По умолчанию используется директория `images`.

Пример:

```shell
python3 post_on_telegram.py --directory my_images --sleeptime 3600
```

### `post_random_photo.py` ###

This script publishes a single photo to your Telegram channel. You can specify a file directly via the `--filepath` argument:

```bash
python3 post_random_photo.py --filepath images/apod/apod_14.jpg
Photo published to Telegram: images/apod/apod_14.jpg
```

If no path is provided, it will select a random image from the `images` folder and its subdirectories. You can also specify a directory from which a random photo will be selected:

```shell
python3 post_random_photo.py --directory my_images
```

## Downloading Space Photos from NASA and SpaceX APIs ##

The project includes three scripts for downloading images from public APIs. Each script saves images to a subdirectory inside `images`, creating the `images` directory if it doesn’t exist.

All three scripts support the following optional arguments:

* `--folder`: directory to save images (default: `images`)
* `--count`: number of images to download (default: `10`)

Example:

```bash
python3 fetch_spacex_images.py --folder test --count 100
SpaceX images saved!
```

### `fetch_spacex_images.py` ###

Downloads images from a specific SpaceX launch. You can specify a `--launch_id`, or omit it to get images from the latest launch:

```bash
python3 fetch_spacex_images.py --launch_id 5eb87d47ffd86e000604b38a
```

If the ID is invalid or not provided:

```bash
Invalid launch ID '5eb87d47ffd86e000604b38a'. Fetching images from the latest launch...
SpaceX images saved!
```

### `fetch_apod_images.py` ###

Fetches random images from NASA's Astronomy Picture of the Day (APOD) API. Requires a NASA API token.

```bash
python3 fetch_apod_images.py
NASA APOD images saved!
```

### `fetch_epic_images.py` ###

Fetches images from NASA’s Earth Polychromatic Imaging Camera (EPIC). By default, it gets 10 photos from 7 days ago. You can adjust the date logic in the function if needed.

```bash
python3 fetch_epic_images.py
NASA EPIC images saved!
```

## Utility Modules ##

### `download_utils.py` ###

Provides shared functionality for downloading photos from all APIs. Includes:

* `fetch_photos()` — downloads all images from a list
* `check_file_extension()` — detects file type from a URL

### `publish_utils.py` ###

Includes helper functions for Telegram publishing:

* `collect_file_paths()` — recursively gathers image paths from a folder
* `publish_single_photo()` — sends a photo to a Telegram channel using the bot API

## Project Purpose ##

This project was created for educational purposes as part of the web development course at [dvmn.org](https://dvmn.org).