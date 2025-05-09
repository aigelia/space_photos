import os


def collect_file_paths(directory):
    """Collects paths to all files in the specified directory and its subdirectories."""
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    return file_paths


def publish_single_photo(bot, chat_id, file_path):
    with open(file_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)
