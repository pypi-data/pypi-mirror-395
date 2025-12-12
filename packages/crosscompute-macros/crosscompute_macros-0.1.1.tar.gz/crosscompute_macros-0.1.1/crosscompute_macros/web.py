import socket
from contextlib import suppress
from functools import partial
from os.path import dirname
from random import randint

import aiofiles
from aiohttp import request
from aiohttp.client_exceptions import ClientError

from .disk import (
    make_folder)
from .error import (
    DiskError,
    WebConnectionError,
    WebRequestError)
from .iterable import (
    drop_null_values)


async def upload(
        target_uri, source_path, client_session=None, chunk_size=1024 * 1024,
        method='PUT', headers=None, params=None):
    fetch = _get_fetch(client_session, method)
    if headers:
        drop_null_values(headers)
    try:
        async with aiofiles.open(source_path, mode='rb') as f:
            async def yield_chunk(chunk_size):
                while (chunk := await f.read(chunk_size)):
                    yield chunk
            async with fetch(
                url=target_uri,
                data=yield_chunk(chunk_size),
                headers=headers,
                params=params,
            ) as response:
                response_status = response.status
                response_text = await response.text()
                if response_status != 200:
                    raise WebRequestError(
                        response_text, uri=target_uri, code=response_status)
    except OSError as e:
        x = 'path is not accessible'
        raise DiskError(x, path=source_path) from e
    except ClientError as e:
        raise WebConnectionError(e, uri=target_uri) from e
    return response_text


async def download(
        target_path, source_uri, client_session=None, chunk_size=1024 * 1024,
        method='GET', headers=None, params=None):
    fetch = _get_fetch(client_session, method)
    if headers:
        drop_null_values(headers)
    try:
        async with fetch(
            url=source_uri, headers=headers, params=params,
        ) as response:
            response_status = response.status
            if response_status != 200:
                raise WebRequestError(
                    await response.text(), uri=source_uri,
                    code=response_status)
            await make_folder(dirname(target_path))
            async with aiofiles.open(target_path, mode='wb') as f:
                async for chunk in response.content.iter_chunked(chunk_size):
                    await f.write(chunk)
    except ClientError as e:
        raise WebConnectionError(e, uri=source_uri) from e


async def make_error(Error, message_text, response=None, error=None):
    error_texts = [message_text]
    kwargs = {}
    if response:
        response_text = (await response.text()).strip()
        if response_text:
            error_texts.append(response_text)
        kwargs['uri'] = response.url
        kwargs['code'] = response.status
    elif error:
        error_text = str(error).strip()
        if error_text:
            error_texts.append(error_text)
        kwargs['uri'] = error.uri
        if hasattr(error, 'code'):
            kwargs['code'] = error.code
    return Error('; '.join(error_texts), **kwargs)


def escape_quotes_html(x):
    with suppress(AttributeError):
        x = x.replace('"', '&#34;').replace("'", '&#39;')
    return x


def escape_quotes_js(x):
    with suppress(AttributeError):
        x = x.replace('"', '\\"').replace("'", "\\'")
    return x


def find_open_port(
        default_port=None,
        minimum_port=1024,
        maximum_port=65535):

    def get_new_port():
        return randint(minimum_port, maximum_port)  # noqa: S311

    port = default_port or get_new_port()
    port_count = maximum_port - minimum_port + 1
    closed_ports = set()
    while True:
        if not is_port_in_use(port):
            break
        closed_ports.add(port)
        if len(closed_ports) == port_count:
            x = (
                'could not find an open port in '
                f'[{minimum_port}, {maximum_port}]')
            raise OSError(x)
        port = get_new_port()
    return port


def is_port_in_use(port):
    # https://stackoverflow.com/a/52872579
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        is_in_use = s.connect_ex(('127.0.0.1', int(port))) == 0
    return is_in_use


def replace_localhost(netloc):
    domain_name = netloc.split(':')[0]
    if domain_name == 'localhost':
        netloc = netloc.replace('localhost', '127.0.0.1')
    return netloc


def _get_fetch(client_session, method_name):
    method_name = method_name.lower()
    if client_session:
        fetch = getattr(client_session, method_name)
    else:
        fetch = partial(request, method=method_name)
    return fetch


# ruff: noqa: PLR2004
