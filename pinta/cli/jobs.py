import os

import click
import requests
import json
import asyncio
from urllib.parse import urlencode
import tarfile
from tempfile import TemporaryFile

from pinta.cli.websocket_client import websocket_connect, websocket_write, websocket_read
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
@click.option('-it', is_flag=True)
@click.argument('id', nargs=1)
@click.argument('command', nargs=1)
def exec(it, id, command):
    url = config.websocket_host + f'/api/jobs/{id}/exec'
    params = {
        'tty': it,
        'command': command,
        'authorization': f'Bearer {config.token}'
    }
    url = url + '?' + urlencode(params)
    asyncio.run(websocket_connect(url))


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


@click.command()
@click.option('-r', is_flag=True)
@click.argument('src')
@click.argument('dst')
def cp(r, src, dst):
    from_path = src.split(':')
    to_path = dst.split(':')
    if len(from_path) == 1 and len(to_path) == 2:
        local_to_remote(from_path[0], int(to_path[0]), to_path[1], r)
    elif len(from_path) == 2 and len(to_path) == 1:
        remote_to_local(int(from_path[0]), from_path[1], to_path[0], r)
    else:
        print('Operation not supported')


def local_to_remote(local_file, id, remote_file, recursive):
    with TemporaryFile() as tar_buffer:
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            tar.add(local_file, arcname=os.path.split(local_file.rstrip('/'))[1])
        tar_buffer.seek(0)
        url = config.websocket_host + f'/api/jobs/{id}/exec'
        params = {
            'tty': False,
            'command': f'tar -C {remote_file} -xf -',
            'authorization': f'Bearer {config.token}'
        }
        url = url + '?' + urlencode(params)
        asyncio.run(websocket_write(url, tar_buffer))


def remote_to_local(id, remote_file, local_file, recursive):
    with TemporaryFile() as tar_buffer:
        url = config.websocket_host + f'/api/jobs/{id}/exec'
        head, tail = os.path.split(remote_file.rstrip('/'))
        params = {
            'tty': False,
            'command': f'tar -C {head} -cf - {tail}',
            'authorization': f'Bearer {config.token}'
        }
        url = url + '?' + urlencode(params)
        asyncio.run(websocket_read(url, tar_buffer))

        tar_buffer.flush()
        tar_buffer.seek(0)

        with tarfile.open(fileobj=tar_buffer, mode='r:') as tar:
            tar.extractall(local_file)

# @main.command()
# def test():
#     url = config.websocket_host + '/api/jobs/ws'
#     asyncio.run(websocket_connect(url))

