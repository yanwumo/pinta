import asyncio
from urllib.parse import urlencode

import click
import requests

from pinta.cli.auth import BearerAuth
from pinta.cli.config.config import config
from pinta.cli.websocket_client import websocket_connect_one_way


@click.command()
@click.argument('id', nargs=1)
@click.option('-r', '--role', default='')
@click.option('-n', '--num', type=int, default=0)
def log(id, role, num):
    url = config.host + f'/api/jobs/{id}/log'
    params = {
        'role': role,
        'num': num
    }
    url = url + '?' + urlencode(params)
    response = requests.get(url, auth=BearerAuth()).json()
    print(response, end='')


@click.command()
@click.argument('id', nargs=1)
@click.option('-r', '--role', default='')
@click.option('-n', '--num', type=int, default=0)
def watch(id, role, num):
    url = config.websocket_host + f'/api/jobs/{id}/watch'
    params = {
        'role': role,
        'num': num,
        'authorization': f'Bearer {config.token}'
    }
    url = url + '?' + urlencode(params)
    asyncio.run(websocket_connect_one_way(url))
