import click
import requests
import json
import asyncio

from pinta.cli.websocket_client import websocket_connect


@click.group()
def pinta():
    pass


@click.command()
@click.option('--user', prompt='Username', help='Username.')
@click.option('--password', prompt=True, hide_input=True, help='Password.')
def login(user, password):
    url = 'https://qedsim.usc.edu/api/login/access-token'
    data = {
        'username': user,
        'password': password
    }
    response = requests.post(url, data=data).json()
    print(response)
    if 'access_token' in response:
        with open('config.json', 'w') as config_file:
            json.dump(response, config_file)


@click.command()
@click.option('--job_id', help='Job id.')
def connect(job_id):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    url = f"wss://qedsim.usc.edu/api/jobs/{job_id}/exec?authorization=Bearer%20{config['access_token']}"
    asyncio.run(websocket_connect(url))


# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)


pinta.add_command(login)
pinta.add_command(connect)


if __name__ == '__main__':
    pinta()
