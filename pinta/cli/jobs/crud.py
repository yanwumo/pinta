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


job_types = {'symmetric', 'ps-worker', 'mpi', 'image-builder'}
job_samples = {
    'symmetric': {
        "name": "",
        "description": "",
        "image": "ubuntu:latest",
        "from_private": False,
        "working_dir": "/",
        "command": 'echo "Hello, world!"; sleep 300',
        "num_replicas": 3,
        "ports": "2222",
        "scheduled": True
    },
    'ps-worker': {
        "name": "",
        "description": "",
        "image": "ubuntu:latest",
        "from_private": False,
        "working_dir": "/",
        "ps_command": 'echo "Hello, PS!"; sleep 300',
        "worker_command": 'echo "Hello, worker!"; sleep 300',
        "num_ps": 1,
        "num_workers": 2,
        "ports": "2222",
        "scheduled": True
    },
    'mpi': {
        "name": "",
        "description": "",
        "image": "ubuntu:latest",
        "from_private": False,
        "working_dir": "/",
        "master_command": 'echo "Hello, master!"; sleep 300',
        "replica_command": 'echo "Hello, replica!"; sleep 300',
        "num_replicas": 2,
        "ports": "2222",
        "scheduled": True
    },
    'image-builder': {
        "name": "",
        "description": "",
        "from_image": "ubuntu:latest",
        "scheduled": True
    }
}


@click.command('job')
@click.option('-t', '--type', required=True, type=click.Choice(job_types, case_sensitive=False))
@click.option('-f', '--file', type=click.File('r'))
def create_job(type, file):
    url = config.host + f'/api/jobs/{type}'
    if file:
        data = file.read()
    else:
        data = click.edit(json.dumps(job_samples[type], indent=4), extension='.json')
        if data is None:
            print('Exited from editor, job not created')
            return
    response = requests.post(url, data=data, auth=BearerAuth()).json()
    print(json.dumps(response, indent=2))
