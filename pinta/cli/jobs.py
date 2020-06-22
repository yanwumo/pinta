import click
import requests
import json
import asyncio
from urllib.parse import urlencode

from pinta.cli.websocket_client import websocket_connect
from pinta.cli.auth import BearerAuth
from pinta.cli.config.config import config


@click.command('jobs')
def get_jobs():
    url = config.host + '/api/jobs/'
    response = requests.get(url, auth=BearerAuth()).json()
    print(json.dumps(response, indent=2))


@click.command('job')
@click.argument('id', nargs=1)
def get_job_by_id(id):
    url = config.host + f'/api/jobs/{id}'
    response = requests.get(url, auth=BearerAuth()).json()
    print(json.dumps(response, indent=2))


@click.command('job')
@click.option('-f', '--file', required=True, type=click.File('r'))
def create_job(file):
    url = config.host + '/api/jobs/'
    data = file.read()
    response = requests.post(url, data=data, auth=BearerAuth()).json()
    print(json.dumps(response, indent=2))


@click.command()
@click.argument('id', nargs=1)
def ssh(id):
    url = config.websocket_host + f'/api/jobs/{id}/exec?authorization=Bearer%20{config.token}'
    asyncio.run(websocket_connect(url))


@click.command()
@click.argument('id', nargs=1)
@click.option('-i', '--image-name', required=True)
def commit(id, image_name):
    url = config.websocket_host + f'/api/jobs/{id}/commit?'
    params = {
        'image_name': image_name,
        'authorization': f'Bearer {config.token}'
    }
    url += urlencode(params)
    asyncio.run(websocket_connect(url))


# @main.command()
# def test():
#     url = config.websocket_host + '/api/jobs/ws'
#     asyncio.run(websocket_connect(url))

