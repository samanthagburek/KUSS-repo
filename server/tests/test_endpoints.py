from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

from data.people import NAME, AFFILIATION, EMAIL

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    resp_json = resp.get_json()
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)


def test_get_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person
        assert AFFILIATION in person
        assert EMAIL in person


#def test_create_people():
#    resp = TEST_CLIENT.put(ep.PEOPLE_EP, "john@who.org", "John Smith", "WHO")
#    resp_json = resp.get_json()
#    for _id, person in resp_json.items():
#        assert isinstance(_id, str)
#        assert len(_id) > 0
#        assert NAME in person
#        assert AFFILIATION in person
#        assert EMAIL in person