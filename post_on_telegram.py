import argparse
import os
from random import shuffle
from time import sleep

from decouple import config
import telegram


def create_parser():
    parser = argparse.ArgumentParser(
        description="Скрипт для автоматической публикации фото в Telegram"
    )
    parser.add_argument(
        "--sleeptime",
        type=int,
        default=None,
        help="Задержка между публикациями в часах"
    )
    return parser


def collect_file_paths(directory="images"):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    shuffle(file_paths)
    return file_paths


def publish_single_photo(bot, chat_id, file_path):
    with open(file_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)


def main():
    parser = create_parser()
    args = parser.parse_args()
    sleeptime_hours = args.sleeptime if args.sleeptime is not None else 4
    post_interval = sleeptime_hours * 3600
    tg_token = config("TG_TOKEN")
    chat_id = config("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    file_paths = collect_file_paths()
    current_index = 0
    while True:
        if current_index >= len(file_paths):
            file_paths = collect_file_paths()
            current_index = 0
        file_path = file_paths[current_index]
        publish_single_photo(bot, chat_id, file_path)
        current_index += 1
        sleep(post_interval)


if __name__ == "__main__":
    main()
