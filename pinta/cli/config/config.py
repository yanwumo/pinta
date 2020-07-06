import configparser
from pathlib import Path


class Config:
    def __init__(self):
        c = configparser.ConfigParser()
        self._file_name = f'{Path(__file__).resolve().parent}/config.ini'
        c.read(self._file_name)

        self.host = c['server']['host']
        self.token = c['server']['token']

    @property
    def host(self):
        return self._host

    @property
    def websocket_host(self):
        return 'ws' + self._host[4:]

    @host.setter
    def host(self, value: str):
        if not value.startswith('http://') and not value.startswith('https://'):
            raise ValueError(f'Illegal hostname: "{value}". Check configuration.')
        if value[-1] == '/':
            value = value[:-1]
        self._host = value

    def write(self):
        c = configparser.ConfigParser()
        c['server'] = dict(
            host=self.host,
            token=self.token
        )
        with open(self._file_name, 'w') as config_file:
            c.write(config_file)
        return self


config = Config()
