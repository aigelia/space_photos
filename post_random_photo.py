import argparse
import os
import random

from decouple import config
import telegram

from publish_utils import collect_file_paths, publish_single_photo


def create_parser():
    parser = argparse.ArgumentParser(
        description="Публикует указанную или случайную фотографию в Telegram"
    )
    parser.add_argument(
        "--filepath",
        help="Путь к конкретной фотографии. Если не указан — будет выбрана случайная."
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    tg_token = config("TG_TOKEN")
    chat_id = config("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    file_path = args.filepath or random.choice(collect_file_paths())
    publish_single_photo(bot, chat_id, file_path)
    print(f"Фото опубликовано: {file_path}")


if __name__ == "__main__":
    main()
