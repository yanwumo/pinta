import asyncio
from urllib.parse import urlencode

import click

from pinta.cli.config.config import config
from pinta.cli.websocket_client import websocket_connect


@click.command()
@click.option('-it', is_flag=True)
@click.option('-r', '--role', default='')
@click.option('-n', '--num', type=int, default=0)
@click.argument('id', nargs=1)
@click.argument('command', nargs=1)
def exec(it, id, role, num, command):
    _exec(it, id, role, num, command)


@click.command()
@click.argument('id', nargs=1)
@click.option('-r', '--role', default='')
@click.option('-n', '--num', type=int, default=0)
def ssh(id, role, num):
    _exec(True, id, role, num, '')


def _exec(it, id, role, num, command):
    url = config.websocket_host + f'/api/jobs/{id}/exec'
    params = {
        'tty': it,
        'role': role,
        'num': num,
        'command': command,
        'authorization': f'Bearer {config.token}'
    }
    url = url + '?' + urlencode(params)
    asyncio.run(websocket_connect(url))
