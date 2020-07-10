import asyncio
from urllib.parse import urlencode

import click

from pinta.cli.config.config import config
from pinta.cli.websocket_client import websocket_connect


@click.command()
@click.option('-it', is_flag=True)
@click.argument('id', nargs=1)
@click.argument('command', nargs=1)
def exec(it, id, command):
    _exec(it, id, command)


@click.command()
@click.argument('id', nargs=1)
def ssh(id):
    _exec(True, id, '/bin/sh')


def _exec(it, id, command):
    url = config.websocket_host + f'/api/jobs/{id}/exec'
    params = {
        'tty': it,
        'command': command,
        'authorization': f'Bearer {config.token}'
    }
    url = url + '?' + urlencode(params)
    asyncio.run(websocket_connect(url))
