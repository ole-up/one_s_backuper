import asyncio
import os
import posixpath

import yadisk_async

ya_disk = yadisk_async.YaDisk(
    token='y0_AgAEA7qkULv3AAjxkwAAAADXvzixOf0e6LtFT4eSyoZWe8fFUQUj9VU')
#UMK token

def recursive_upload(from_dir: str, to_dir: str,
                     n_parallel_requests=5):
    """Рекурсивная загрузка файлов на Я.Диск"""
    loop = asyncio.get_event_loop()
    try:
        async def upload_files(queue):
            while queue:
                in_path, out_path = queue.pop(0)
                print("Uploading %s -> %s" % (in_path, out_path))
                try:
                    await ya_disk.upload(in_path, out_path)
                except yadisk_async.exceptions.PathExistsError:
                    print("%s already exists" % (out_path,))

        async def create_dirs(queue):
            while queue:
                path = queue.pop(0)

                print("Creating directory %s" % (path,))

                try:
                    await ya_disk.mkdir(path)
                except yadisk_async.exceptions.PathExistsError:
                    print("%s already exists" % (path,))

        mkdir_queue = []
        upload_queue = []

        print("Creating directory %s" % (to_dir,))

        try:
            loop.run_until_complete(ya_disk.mkdir(to_dir))
        except yadisk_async.exceptions.PathExistsError:
            print("%s already exists" % (to_dir,))

        for root, dirs, files in os.walk(from_dir):
            rel_dir_path = root.split(from_dir)[1].strip(os.path.sep)
            rel_dir_path = rel_dir_path.replace(os.path.sep, "/")
            dir_path = posixpath.join(to_dir, rel_dir_path)

            for dirname in dirs:
                mkdir_queue.append(posixpath.join(dir_path, dirname))

            for filename in files:
                out_path = posixpath.join(dir_path, filename)
                rel_dir_path_sys = rel_dir_path.replace("/", os.path.sep)
                in_path = os.path.join(from_dir, rel_dir_path_sys, filename)

                upload_queue.append((in_path, out_path))

            tasks = [upload_files(upload_queue) for i in
                     range(n_parallel_requests)]
            tasks.extend(
                create_dirs(mkdir_queue) for i in range(n_parallel_requests))

            loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.run_until_complete(ya_disk.close())



def list_dirs(path):
    """Список папок по заданному пути"""
    loop = asyncio.get_event_loop()

    async def listdirs(path):
        return [i async for i in await ya_disk.listdir(path)]

    list_dir = loop.run_until_complete(listdirs(path))
    loop.run_until_complete(ya_disk.close())
    loop.close()
    return list_dir


async def remove_file(path):
    await ya_disk.remove(path, permanently=True)


if __name__ == '__main__':
    print(list_dirs("/dyachenko"))
