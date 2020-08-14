import json
import yaml

import click
import requests

from pinta.cli.auth import BearerAuth
from pinta.cli.config.config import config


@click.command('images')
def get_images():
    url = config.host + '/api/images/'
    response = requests.get(url, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))


@click.command('image')
@click.argument('id', nargs=1)
def get_image_by_id(id):
    url = config.host + f'/api/images/{id}'
    response = requests.get(url, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))


@click.command('image')
@click.argument('id', nargs=1)
def delete_image_by_id(id):
    url = config.host + f'/api/images/{id}'
    response = requests.delete(url, auth=BearerAuth()).json()
    print(yaml.dump(response, sort_keys=False))

