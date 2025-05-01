import argparse
from time import sleep

from decouple import config
import telegram

from post_helper import collect_file_paths, publish_single_photo


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
