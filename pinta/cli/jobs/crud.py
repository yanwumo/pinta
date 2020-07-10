import json

import click
import requests

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