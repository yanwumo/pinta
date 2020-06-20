import click
import requests

from pinta.cli.config.config import config


@click.command()
@click.option('--user', prompt='Username', help='Username.')
@click.option('--password', prompt=True, hide_input=True, help='Password.')
def login(user, password):
    url = config.host + '/api/login/access-token'
    data = {
        'username': user,
        'password': password
    }
    response = requests.post(url, data=data).json()
    if 'access_token' in response:
        config.token = response['access_token']
        config.write()
        print('Success')
