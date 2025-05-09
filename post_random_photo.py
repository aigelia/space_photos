import argparse
import os
import random

from decouple import config
import telegram

from publish_utils import collect_file_paths, publish_single_photo


def create_parser():
    parser = argparse.ArgumentParser(
        description="Publishes a specified or random photo to a Telegram channel"
    )
    parser.add_argument(
        "--filepath",
        help="Path to a specific image. If not specified, a random one will be selected."
    )
    parser.add_argument(
        "--folder",
        default="images",
        help="Directory to select a random image from"
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    tg_token = config("TG_TOKEN")
    chat_id = config("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    file_paths = collect_file_paths(args.folder)
    file_path = args.filepath or random.choice(file_paths)
    publish_single_photo(bot, chat_id, file_path)
    print(f"Photo published to Telegram: {file_path}")


if __name__ == "__main__":
    main()
