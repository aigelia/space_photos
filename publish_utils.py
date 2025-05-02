import os
import random


def collect_file_paths(directory="images"):
    """Собирает пути ко всем файлам из указанной директории и её поддиректорий."""
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    return file_paths


def shuffle_file_paths(file_paths):
    """Перемешивает список путей к файлам."""
    random.shuffle(file_paths)
    return file_paths


def publish_single_photo(bot, chat_id, file_path):
    with open(file_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)