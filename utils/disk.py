import datetime
import os
import shutil
from pathlib import Path

import config


def clear_folder(path_to_folder: Path):
    for filename in os.listdir(path_to_folder):
        file_path = os.path.join(path_to_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def delete_folder(path: Path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        print('Указанный путь не является папкой. Удаление невозможно.')


def get_list_folder_for_clean(path: str):
    folder_for_clean = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dir_date = datetime.datetime.strptime(dir, '%Y-%m-%d').date()
            if (
                    datetime.datetime.now().date() - dir_date) > datetime.timedelta(
                    days=config.HOW_LONG_KEEP_BACKUP):
                if config.KEEP_QUARTERLY_BACKUP:
                    if dir_date.day == 1 and dir_date.month in [1, 4, 7, 10]:
                        continue
                    folder_for_clean.append(Path(os.path.join(root, dir)))
    return folder_for_clean


if __name__ == '__main__':
    folder_list = get_list_folder_for_clean('C:\\backup')
    for folder in folder_list:
        delete_folder(folder)
