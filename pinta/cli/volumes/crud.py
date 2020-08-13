import json
import yaml

import click
import requests

from pinta.cli.auth import BearerAuth
from pinta.cli.config.config import config


@click.command('volumes')
def get_volumes():
    url = config.host + '/api/volumes/'
    response = requests.get(url, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))


@click.command('volume')
@click.argument('id', nargs=1)
def get_volume_by_id(id):
    url = config.host + f'/api/volumes/{id}'
    response = requests.get(url, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))


volume_sample = {
    "name": "",
    "description": "",
    "capacity": "100Mi"
}


@click.command('volume')
@click.option('-f', '--file', type=click.File('r'))
def create_volume(file):
    url = config.host + f'/api/volumes/'
    if file:
        data = file.read()
    else:
        data = click.edit(json.dumps(volume_sample, indent=4), extension='.yaml')
        if data is None:
            print('Exited from editor, volume not created')
            return
    response = requests.post(url, data=data, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))


@click.command('volume')
@click.argument('id', nargs=1)
def delete_volume_by_id(id):
    url = config.host + f'/api/volumes/{id}'
    response = requests.delete(url, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))

