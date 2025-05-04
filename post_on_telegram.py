import argparse
import random
from time import sleep

from decouple import config
import telegram

from publish_utils import collect_file_paths, publish_single_photo


def create_parser():
    parser = argparse.ArgumentParser(
        description="Скрипт для автоматической публикации фото в Telegram"
    )
    parser.add_argument(
        "--sleeptime",
        type=int,
        default=3600 * 4,
        help="Задержка между публикациями в секундах (по умолчанию 4 часа)"
    )
    parser.add_argument(
        "--folder",
        default="images",
        help="Директория с изображениями для публикации"
    )
    return parser


def post_photos(bot, chat_id, post_interval, directory):
    while True:
        file_paths = collect_file_paths(directory)
        random.shuffle(file_paths)
        for file_path in file_paths:
            try:
                publish_single_photo(bot, chat_id, file_path)
            except telegram.error.NetworkError:
                print("Сетевая ошибка. Ждём 30 секунд перед повтором.")
                sleep(30)
                continue
            sleep(post_interval)


def main():
    parser = create_parser()
    args = parser.parse_args()
    tg_token = config("TG_TOKEN")
    chat_id = config("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    post_interval = args.sleeptime
    directory = args.folder
    post_photos(bot, chat_id, post_interval, directory)


if __name__ == "__main__":
    main()
