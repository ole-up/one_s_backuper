import asyncio
import os
import posixpath

import yadisk

ya_disk = yadisk.AsyncYaDisk(token='y0_AgAEA7qkULv3AAjxkwAAAADXvzixOf0e6LtFT4eSyoZWe8fFUQUj9VU', session="aiohttp")


async def recursive_upload(from_dir: str, to_dir: str, n_parallel_requests: int = 5):
    async with yadisk as client:
        async def upload_files(queue):
            while queue:
                in_path, out_path = queue.pop(0)

                print(f"Uploading {in_path} -> {out_path}")

                try:
                    await client.upload(in_path, out_path)
                except yadisk.exceptions.PathExistsError:
                    print(f"{out_path} already exists")

        async def create_dirs(queue):
            while queue:
                path = queue.pop(0)

                print(f"Creating directory {path}")

                try:
                    await client.mkdir(path)
                except yadisk.exceptions.PathExistsError:
                    print(f"{path} already exists")

        mkdir_queue = []
        upload_queue = []

        print(f"Creating directory {to_dir}")

        try:
            await client.mkdir(to_dir)
        except yadisk.exceptions.PathExistsError:
            print(f"{to_dir} already exists")

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

            tasks = [upload_files(upload_queue) for i in range(n_parallel_requests)]
            tasks.extend(create_dirs(mkdir_queue) for i in range(n_parallel_requests))

            await asyncio.gather(*tasks)


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
    async with ya_disk as client:
        await client.remove(path, permanently=True)


if __name__ == '__main__':
    print(list_dirs("/dyachenko"))
