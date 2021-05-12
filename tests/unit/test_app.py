"""pytest tests for basic app functionality"""

import json
import os.path

import pytest


def test_read_root(anon_client):
    """The site root redirects to the Swagger docs"""
    resp = anon_client.get("/")
    assert resp.status_code == 200
    assert len(resp.history) == 1
    prev_resp = resp.history[0]
    assert prev_resp.status_code == 307  # Temporary Redirect
    assert prev_resp.headers["location"] == "./docs"


def test_read_version(anon_client):
    """__version__ returns the contents of version.json."""
    here = os.path.dirname(__file__)
    root_dir = os.path.dirname(os.path.dirname(here))
    version_path = os.path.join(root_dir, "version.json")
    version_contents = open(version_path, "r").read()
    expected = json.loads(version_contents)
    resp = anon_client.get("/__version__")
    assert resp.status_code == 200
    assert resp.json() == expected


def test_crash_authorized(client):
    """The endpoint /__crash__ can be used to test Sentry integration."""
    with pytest.raises(RuntimeError):
        client.get("/__crash__")


def test_crash_unauthorized(anon_client):
    """The endpoint /__crash__ can not be used without credentials."""
    resp = anon_client.get("/__crash__")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}
