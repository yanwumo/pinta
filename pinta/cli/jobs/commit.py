import asyncio
from urllib.parse import urlencode

import click

from pinta.cli.config.config import config
from pinta.cli.websocket_client import websocket_connect


@click.command()
@click.argument('id', nargs=1)
@click.option('-i', '--image-name', required=True)
def commit(id, image_name):
    url = config.websocket_host + f'/api/jobs/{id}/commit'
    params = {
        'image_name': image_name,
        'authorization': f'Bearer {config.token}'
    }
    url = url + '?' + urlencode(params)
    asyncio.run(websocket_connect(url))