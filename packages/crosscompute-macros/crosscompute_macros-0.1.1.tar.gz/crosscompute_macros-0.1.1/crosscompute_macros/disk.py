import json
from contextlib import suppress
from logging import getLogger
from os import pathconf
from os.path import dirname, join, normpath

import aiofiles
import aiofiles.os

from .error import DiskError, ParsingError
from .iterable import LRUDict
from .random import make_random_string


class FileCache(LRUDict):

    def __init__(self, *args, load, length: int, **kwargs):
        super().__init__(*args, length=length, **kwargs)
        self._load = load

    async def set(self, path, d):
        t = await get_modification_time(path)
        value = t, d
        super().__setitem__(str(path), value)

    async def get(self, path):
        path = str(path)
        if path in self:
            old_t, d = super().__getitem__(path)
            new_t = await get_modification_time(path)
            if old_t == new_t:
                return d
        x = await self._load(path)
        await self.set(path, x)
        return x


async def make_random_folder(
        base_folder, name_length=16, with_fixed_length=False,
        length_increment=8, retry_count=3):
    retry_index = 0
    while True:
        name = chop_name(make_random_string(name_length))
        folder = join(base_folder, name)
        try:
            await make_folder(folder, with_existing=False)
            break
        except FileExistsError as e:
            if retry_index < retry_count:
                retry_index += 1
                L.debug(f'folder {retry_index=}', path=base_folder)
                continue
            if with_fixed_length:
                x = (
                    'folder is nearing capacity and cannot support more '
                    'random folders')
                raise DiskError(x, path=base_folder) from e
            name_length += length_increment
            L.debug(f'folder {name_length=}', path=base_folder)
    return folder


async def make_folder(folder, with_existing=True):
    await aiofiles.os.makedirs(folder, exist_ok=with_existing)
    return folder


async def copy_path(target_path, source_path):
    byte_count = await get_byte_count(source_path)
    await make_folder(target_path.parent)
    async with aiofiles.open(
        target_path, mode='wb',
    ) as t, aiofiles.open(
        source_path, mode='rb',
    ) as s:
        await aiofiles.os.sendfile(t.fileno(), s.fileno(), 0, byte_count)
    return target_path


async def get_byte_count(path):
    s = await aiofiles.os.stat(path)
    return s.st_size


async def save_raw_text(path, text):
    await make_folder(dirname(path))
    async with aiofiles.open(path, mode='wt') as f:
        await f.write(text)
    return path


async def load_raw_text(path):
    try:
        async with aiofiles.open(path, mode='rt') as f:
            text = await f.read()
    except OSError as e:
        x = f'path is not accessible; {e}'
        raise DiskError(x, path=path) from e
    return text.rstrip()


async def save_raw_json(path, dictionary):
    await make_folder(dirname(path))
    async with aiofiles.open(path, mode='wt') as f:
        await f.write(json.dumps(dictionary))


async def load_raw_json(path):
    try:
        async with aiofiles.open(path, mode='rt') as f:
            dictionary = json.loads(await f.read())
    except OSError as e:
        x = f'path is not accessible; {e}'
        raise DiskError(x, path=path) from e
    except json.JSONDecodeError as e:
        x = f'file is not valid json; {e}'
        raise ParsingError(x, path=path) from e
    return dictionary


async def update_raw_json(path, dictionary):
    if await is_existing_path(path):
        async with aiofiles.open(path, mode='r+t') as f:
            with suppress(json.JSONDecodeError):
                dictionary = json.loads(await f.read()) | dictionary
            await f.seek(0)
            await f.write(json.dumps(dictionary))
            await f.truncate()
    else:
        await save_raw_json(path, dictionary)
    return dictionary


async def make_soft_link(target_path, source_path):
    await aiofiles.os.symlink(source_path, target_path)


async def make_hard_link(target_path, source_path):
    await aiofiles.os.link(source_path, target_path)


async def get_real_path(path):
    path = await get_absolute_path(path)
    original_path = path
    paths = [path]
    while await is_link_path(path):
        path = await get_absolute_path(join(
            dirname(path), await aiofiles.os.readlink(path)))
        if path in paths:
            x = 'file is a circular symlink'
            raise DiskError(x, path=original_path)
        paths.append(path)
    return path


async def get_absolute_path(path):
    return await aiofiles.os.path.abspath(path)


async def is_path_in_folder(path, folder):
    try:
        path = await get_real_path(path)
        folder = await get_real_path(folder)
    except DiskError as e:
        L.debug(e)
        return False
    return path.startswith(folder)


def is_contained_path(path):
    folder = '_'
    return normpath(join(folder, path)).startswith(folder)


def chop_name(name):
    parts = []
    name_length = len(name)
    folder_count = name_length // MAXIMUM_FILE_NAME_LENGTH
    for i in range(folder_count):
        a = MAXIMUM_FILE_NAME_LENGTH * i
        b = MAXIMUM_FILE_NAME_LENGTH * (i + 1)
        parts.append(name[a:b])
    parts.append(name[MAXIMUM_FILE_NAME_LENGTH * folder_count:])
    return '/'.join(parts)


def get_folder(path, relative_path):
    return str(path).rsplit(relative_path)[0]


get_modification_time = aiofiles.os.path.getmtime
is_existing_path = aiofiles.os.path.exists
is_file_path = aiofiles.os.path.isfile
is_folder_path = aiofiles.os.path.isdir
is_link_path = aiofiles.os.path.islink
is_same_path = aiofiles.os.path.samefile
list_paths = aiofiles.os.listdir
remove_path = aiofiles.os.unlink


L = getLogger(__name__)
MAXIMUM_FILE_NAME_LENGTH = pathconf('/', 'PC_NAME_MAX')
