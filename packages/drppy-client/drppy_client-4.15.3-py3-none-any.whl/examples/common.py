import json
import os

import click

from datetime import date, datetime
from drppy_client.configuration import Configuration
from drppy_client.models.machine import Machine
from drppy_client.models.content import Content
from drppy_client.models.content_summary import ContentSummary
from drppy_client.models.param import Param
from drppy_client.models.profile import Profile
from drppy_client.models.subnet import Subnet


def json_serialize(obj):
    """JSON serializer for drppy_client types.
    Makes it so the datetime as well as lists of
    drppy_client models stuff don't bork the
    default json serializer.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Machine):
        return obj.to_dict()
    if isinstance(obj, Content):
        return obj.to_dict()
    if isinstance(obj, ContentSummary):
        return obj.to_dict()
    if isinstance(obj, Param):
        return obj.to_dict()
    if isinstance(obj, Profile):
        return obj.to_dict()
    if isinstance(obj, Subnet):
        return obj.to_dict()
    raise TypeError("Type {} not serializable".format(type(obj)))


def common_options(func):

    def wrapper(ctx, endpoint, token, key, *args, **kwargs):
        if ctx.obj is None:
            ctx.obj = {}

        return ctx.invoke(func, ctx, *args, **kwargs)
    return wrapper


class Config(object):
    def __init__(self, host=None, token=None, key=None, verify_ssl=False,
                 debug=False):
        if host is None:
            self.host = os.getenv(
                "RS_ENDPOINT",
                "https://127.0.0.1:8092/api/v3"
            )
        if token is None:
            self.token = os.getenv("RS_TOKEN", None)
        if key is None:
            self.key = os.getenv("RS_KEY", None)
        if self.token is None and self.key is None:
            self.key = "rocketskates:r0cketsk8ts"
        if self.host is not None and self.host.endswith('/'):
            self.host = self.host[:-1]
        if self.host is not None and not self.host.endswith("/api/v3"):
            self.host = self.host + "/api/v3"
        # Check if token is none, if so it needs to be an empty dict for
        # the constructor to work
        if self.token is None:
            self.token = {}
        self.api_config = Configuration()
        self.api_config.host = self.host
        self.api_config.verify_ssl = verify_ssl
        self.api_config.api_key = self.token
        if self.key:
            user, passwd = self.key.split(":")
            self.api_config.username = user
            self.api_config.password = passwd
        self.api_config.debug = debug
