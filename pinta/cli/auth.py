import requests.auth

from pinta.cli.config.config import config


class BearerAuth(requests.auth.AuthBase):
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + config.token
        return r
