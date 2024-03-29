import datetime
import os
import posixpath
import time

import yadisk
from progress.bar import IncrementalBar

import config

yandex_disk = yadisk.YaDisk(token=config.YADISK_TOKEN, session='httpx')
# yandex_disk.get_meta(
#     '/',
#     n_retries=5,
#     httpx_args={
#         "verify": False,
#     }
# )


# UMK token


def recursive_upload(from_dir, to_dir):
    for root, dirs, files in os.walk(from_dir):
        p = root.split(from_dir)[1].strip(os.path.sep)
        dir_path = posixpath.join(to_dir, p)
        counter = 1
        while counter < 5:
            try:
                yandex_disk.mkdir(dir_path)
                print(f'Создаем папку {dir_path}')
                break
            except yadisk.exceptions.PathExistsError:
                print(f'Папка {dir_path} уже существует')
                break
            except yadisk.exceptions.ResourceIsLockedError:
                # try again
                print(f'{counter} попытка создания папки прошла неудачно, пробуем еще раз')
                counter += 1
                continue
        bar = IncrementalBar('Выгрузка файлов на Я.Диск: ', max=len(files))
        for file in files:
            file_path = posixpath.join(dir_path, file)
            p_sys = p.replace("/", os.path.sep)
            in_path = os.path.join(from_dir, p_sys, file)
            counter = 1
            while counter < 5:
                try:
                    yandex_disk.upload(in_path, file_path)
                    break
                except yadisk.exceptions.PathExistsError:
                    break
                except yadisk.exceptions.ResourceIsLockedError:
                    # try again
                    print(f'{counter} попытка загрузки прошла неудачно, пробуем еще раз')
                    counter += 1
                    continue
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


def empty_trash():
    with yandex_disk as client:
        print('Очищаем корзину Я.Диска...')
        operation = client.remove_trash('/')
        print('Это займет некоторое время...')

        if operation is None:
            print('Корзина очищена.')
            return

        while True:
            status = client.get_operation_status(operation.href)

            if status == 'in-progress':
                time.sleep(5)
                print('Все еще ждем...')
            elif status == 'success':
                print('Успешно!')
                break
            else:
                print(f'Получен странный статус выполнения операции: {repr(status)}')
                print('Это не нормально')
                break


if __name__ == '__main__':
    folder_list = get_list_folder_for_clean('test')
    print(folder_list)
    for folder in folder_list:
        delete_folder(folder)
