import argparse
import os
from random import shuffle
from time import sleep

from decouple import config
import telegram


def create_parser():
    parser = argparse.ArgumentParser(
        description='Утилита для публикации фото в Telegram'
    )
    parser.add_argument(
        '--sleeptime',
        type=int,
        default=None,
        help='Задержка между публикациями в часах. Приоритетнее переменной окружения POST_INTERVAL.'
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
    with open(file_path, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.sleeptime is not None:
        post_interval = args.sleeptime * 3600
    else:
        post_interval = config('POST_INTERVAL', default=14400, cast=int)
    tg_token = config('TG_TOKEN')
    bot = telegram.Bot(token=tg_token)
    chat_id = '@dvmn_space_photos'
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


if __name__ == '__main__':
    main()
