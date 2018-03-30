# Copyright 2018 Zegami Ltd

"""Tools for making http requests."""

import requests
import sys


API_START_FORMAT = "{prefix}/api/v0/project/{project_id}/"

class TokenEndpointAuth(requests.auth.AuthBase):
    """Request auth that adds bearer token for specific endpoint only."""

    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def __call__(self, request):
        if request.url.startswith(self.endpoint):
            request.headers["Authorization"] = "Bearer {}".format(self.token)
        return request


def get_api_url(url_prefix, project_id):
    return API_START_FORMAT.format(
        prefix=url_prefix,
        project_id=project_id)

def make_session(auth=None):
    """Create a session object with optional auth handling."""
    session = requests.Session()
    session.auth = auth
    return session


def get(log, session, url):
    """Get a json response."""
    with session.get(url) as response:
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log.error(str(e))
            sys.exit(1)


def post_json(session, url, python_obj):
    """Send a json request and decode json response."""
    with session.post(url, json=python_obj) as response:
        response.raise_for_status()
        return response.json()


def post_file(log, session, url, name, filelike, mime):
    """Send a data file."""
    details = (name, filelike, mime)
    with session.post(url, files={'file': details}) as response:
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log.error(str(e))
            sys.exit(1)


def delete(log, session, url):
    """Get a json response."""
    with session.delete(url) as response:
        try:
            response.raise_for_status()
        except requests.RequestException as e:
            log.error(str(e))
            sys.exit(1)


def put_file(session, url, filelike, mimetype):
    """Put binary content and decode json respose."""
    headers = {'Content-Type': mimetype}
    with session.put(url, data=filelike, headers=headers) as response:
        response.raise_for_status()
        return response.json()


def put_json(session, url, python_obj):
    """Put json content and decode json response."""
    with session.put(url, json=python_obj) as response:
        response.raise_for_status()
        return response.json()
