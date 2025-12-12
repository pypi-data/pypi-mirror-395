import asyncio
import json
from logging import getLogger

from starlette.templating import Jinja2Templates


class TemplateResponseFactory(Jinja2Templates):

    def __init__(self, environment, context_processors=None):
        'Assume nothing about the template environment.'
        self.env = environment
        self.context_processors = context_processors or []


async def yield_map_while_connected(websocket, timeout_in_seconds=1):
    async for x in yield_packet_while_connected(websocket, timeout_in_seconds):
        if x and 'text' in x:
            try:
                x = json.loads(x['text'])
            except json.JSONDecodeError:
                x = {}
            else:
                if not isinstance(x, dict):
                    x = {}
        else:
            x = {}
        yield x


async def yield_packet_while_connected(websocket, timeout_in_seconds=1):
    while True:
        try:
            packet = await asyncio.wait_for(
                websocket.receive(), timeout=timeout_in_seconds)
        except TimeoutError:
            yield
        except RuntimeError:
            break
        else:
            if packet['type'] == 'websocket.disconnect':
                break
            yield packet


L = getLogger(__name__)
