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
from data.text import TITLE, TEXT

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


def test_read():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person
        assert AFFILIATION in person
        assert EMAIL in person


def test_text_read():
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    resp_json = resp.get_json()
    for _id, thing in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert TITLE in thing
        assert TEXT in thing

def test_update_people():
   resp = TEST_CLIENT.get(ep.PEOPLE_EP)
   resp_json = resp.get_json()
   for _id, person in resp_json.items():
       assert isinstance(_id, str)
       assert len(_id) > 0
       assert NAME in person
       assert AFFILIATION in person
       assert EMAIL in person


def test_create_people():
   person_data ={ 
        NAME: "John Smith",
        AFFILIATION: "WHO",
        EMAIL: "john@who.org"
    }

   resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=person_data)
   resp_json = resp.get_json()
   assert resp_json is not None, f'Expected JSON response, but got None. Response text: {resp.data.decode()}'

   assert "return" in resp_json, "Expected 'return' in response"
   assert resp_json["return"] == person_data[EMAIL], f"Expected return to be {person_data[EMAIL]}, but got {resp_json['return']}"


def test_delete_people():
   # creating a person to make sure the person we are trying to delete, exists
   person_data ={ 
        NAME: "Jane Street",
        AFFILIATION: "YOU",
        EMAIL: "jane@you.org"
    }
    
   create_resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=person_data)
   create_resp_json = create_resp.get_json()
   created_email = create_resp_json.get("return")
 
   assert created_email == person_data[EMAIL], f"Expected return to be {person_data[EMAIL]}, but got {resp_json['return']}"

   del_resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{created_email}')
   del_resp_json = delete_resp.get_json()

   assert "Deleted" in del_resp_json, "Expected 'Deleted' in response"
   assert del_resp_json["Deleted"] == created_email, f"Expected deleted ID to be {created_email} but got {del_resp_json['Deleted']}"

   # verifying if deleted
   read_resp = TEST_CLIENT.get(ep.PEOPLE_EP)
   read_resp_json = read_resp.get_json()
   
   assert created_email not in read_resp_json, "Person still found after delete"
