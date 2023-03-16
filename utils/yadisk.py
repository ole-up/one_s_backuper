import os
import posixpath

import yadisk
from progress.bar import IncrementalBar

from config import YADISK_TOKEN

ya_disk = yadisk.YaDisk(
    token=YADISK_TOKEN)


# UMK token


def recursive_upload(from_dir, to_dir):
    for root, dirs, files in os.walk(from_dir):
        p = root.split(from_dir)[1].strip(os.path.sep)
        dir_path = posixpath.join(to_dir, p)
        try:
            ya_disk.mkdir(dir_path)
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
                ya_disk.upload(in_path, file_path)
            except yadisk.exceptions.PathExistsError:
                pass
            bar.next()
        bar.finish()


if __name__ == '__main__':
    pass
