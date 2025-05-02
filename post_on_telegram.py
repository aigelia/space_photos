import argparse
from time import sleep

from decouple import config
import telegram

from publish_utils import collect_file_paths, publish_single_photo, shuffle_file_paths


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


def post_photos(bot, chat_id, post_interval, file_paths):
    current_index = 0
    while True:
        if current_index >= len(file_paths):
            file_paths = collect_file_paths()
            file_paths = shuffle_file_paths(file_paths)
            current_index = 0
        file_path = file_paths[current_index]
        publish_single_photo(bot, chat_id, file_path)
        current_index += 1
        sleep(post_interval)


def main():
    parser = create_parser()
    args = parser.parse_args()
    tg_token = config("TG_TOKEN")
    chat_id = config("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    sleeptime_hours = args.sleeptime if args.sleeptime is not None else 4
    post_interval = sleeptime_hours * 3600
    file_paths = collect_file_paths()
    file_paths = shuffle_file_paths(file_paths)
    post_photos(bot, chat_id, post_interval, file_paths)


if __name__ == "__main__":
    main()
