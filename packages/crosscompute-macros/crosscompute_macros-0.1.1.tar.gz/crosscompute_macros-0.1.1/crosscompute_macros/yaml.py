import aiofiles
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from .error import DiskError, FormattingError, ParsingError


async def load_raw_yaml(path, with_comments=False):
    yaml = YAML(typ='rt' if with_comments else 'safe')
    try:
        async with aiofiles.open(path, mode='rt') as f:
            dictionary = yaml.load(await f.read())
    except OSError as e:
        x = f'path is not accessible; {e}'
        raise DiskError(x, path=path) from e
    except YAMLError as e:
        x = f'file is not yaml; {e}'
        raise ParsingError(x, path=path) from e
    return dictionary or {}


async def save_raw_yaml(path, x, with_comments=False):
    yaml = YAML(typ=['rt' if with_comments else 'safe', 'bytes'])
    try:
        async with aiofiles.open(path, mode='wb') as f:
            await f.write(yaml.dump_to_bytes(x))
    except OSError as e:
        x = f'path is not accessible; {e}'
        raise DiskError(x, path=path) from e
    except YAMLError as e:
        x = f'value cannot be yaml; {e}'
        raise FormattingError(x, path=path) from e


def sync_load_raw_yaml(path, with_comments=False):
    yaml = YAML(typ='rt' if with_comments else 'safe')
    try:
        with path.open(mode='rt') as f:
            dictionary = yaml.load(f.read())
    except OSError as e:
        x = f'path is not accessible; {e}'
        raise DiskError(x, path=path) from e
    except YAMLError as e:
        x = f'file is not valid yaml; {e}'
        raise ParsingError(x, path=path) from e
    return dictionary or {}


def sync_save_raw_yaml(path, x, with_comments=False):
    yaml = YAML(typ=['rt' if with_comments else 'safe', 'bytes'])
    try:
        with path.open(mode='wb') as f:
            f.write(yaml.dump_to_bytes(x))
    except OSError as e:
        x = f'path is not accessible; {e}'
        raise DiskError(x, path=path) from e
    except YAMLError as e:
        x = f'value cannot be yaml; {e}'
        raise FormattingError(x, path=path) from e
