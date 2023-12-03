import datetime
import os
import posixpath

import yadisk
from progress.bar import IncrementalBar

import config

yandex_disk = yadisk.YaDisk(
    token=config.YADISK_TOKEN)


# UMK token


def recursive_upload(from_dir, to_dir):
    for root, dirs, files in os.walk(from_dir):
        p = root.split(from_dir)[1].strip(os.path.sep)
        dir_path = posixpath.join(to_dir, p)
        try:
            yandex_disk.mkdir(dir_path)
            print(f'Создаем папку {dir_path}')
        except yadisk.exceptions.PathExistsError:
            print(f'Папка {dir_path} уже существует')
        bar = IncrementalBar('Выгрузка файлов на Я.Диск: ', max=len(files))
        for file in files:
            file_path = posixpath.join(dir_path, file)
            p_sys = p.replace("/", os.path.sep)
            in_path = os.path.join(from_dir, p_sys, file)
            try:
                # print(f'Загружаем {in_path} -> {file_path}')
                yandex_disk.upload(in_path, file_path)
            except yadisk.exceptions.PathExistsError:
                pass
            bar.next()
        bar.finish()


def get_list_folder_for_clean(path: str):
    folder_for_clean = []
    if yandex_disk.is_dir(path):
        folder_list = [folder_name.name for folder_name in
                       list(yandex_disk.listdir(path))]
        for folder in folder_list:
            folder_date = datetime.datetime.strptime(folder, '%Y-%m-%d').date()
            if (datetime.datetime.now().date() - folder_date) > datetime.timedelta(days=config.HOW_LONG_KEEP_BACKUP):
                if config.KEEP_QUARTERLY_BACKUP:
                    if folder_date.day == 1 and folder_date.month in [1, 4, 7, 10]:
                        continue
                folder_for_clean.append(posixpath.join(path, folder))
                print(f'Folder {folder} add to delete')
    return folder_for_clean


def delete_folder(path):
    try:
        yandex_disk.remove(path)
    except yadisk.exceptions.PathNotFoundError:
        print(f'Папка {path} не найдена на Я.Диске')

if __name__ == '__main__':
    folder_list = get_list_folder_for_clean('test')
    print(folder_list)
    for folder in folder_list:
        delete_folder(folder)
