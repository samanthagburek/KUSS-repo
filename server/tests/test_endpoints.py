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

from data.people import NAME, AFFILIATION, EMAIL, ROLES
from data.text import KEY, TITLE, TEXT
from data.roles import TEST_CODE

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
        EMAIL: "john@who.org",
        NAME: "John Smith",
        AFFILIATION: "WHO",
        ROLES: TEST_CODE
    }

   resp = TEST_CLIENT.put(ep.PEOPLE_EP, json=person_data)
   resp_json = resp.get_json()
   assert resp_json is not None, f'Expected JSON response, but got None. Response text: {resp.data.decode()}'

   assert "return" in resp_json, "Expected 'return' in response"
   assert resp_json["return"] == person_data[EMAIL], f"Expected return to be {person_data[EMAIL]}, but got {resp_json['return']}"


def test_delete_people():
   # creating a person to make sure the person we are trying to delete, exists
   person_data ={
        EMAIL: "jane@you.org",
        NAME: "Jane Street",
        AFFILIATION: "YOU",
        ROLES: TEST_CODE
    }
   person_data_email ={
        EMAIL: "jane@you.org",
    }
    
   create_resp = TEST_CLIENT.put(ep.PEOPLE_EP, json=person_data)
   create_resp_json = create_resp.get_json()
   created_email = create_resp_json.get("return")
 
   assert created_email == person_data[EMAIL], f"Expected return to be {person_data[EMAIL]}, but got {create_resp_json['return']}"

   del_resp = TEST_CLIENT.delete(ep.PEOPLE_EP, json=person_data_email)
  
   del_resp_json = del_resp.get_json()
   print(del_resp_json)
   
   assert "Deleted" in del_resp_json.get("Message"), f"Expected 'Deleted' in response, but got {del_resp_json['Message']}"
   assert created_email in del_resp_json["return"] == created_email, f"Expected deleted ID to be {created_email} but got {del_resp_json['return']}"

   # verifying if deleted
   read_resp = TEST_CLIENT.get(ep.PEOPLE_EP)
   read_resp_json = read_resp.get_json()
   
   assert created_email not in read_resp_json, "Person still found after delete"


def test_text_read():
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    resp_json = resp.get_json()
    for _id, thing in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert TITLE in thing
        assert TEXT in thing

def test_create_text():
   text_data ={ 
        KEY: "CreatePage",
        TITLE: "Create-Test Page",
        TEXT: "This is to test text creation."
    }

   resp = TEST_CLIENT.put(ep.TEXT_EP, json=text_data)
   resp_json = resp.get_json()
   assert resp_json is not None, f'Expected JSON response, but got None. Response text: {resp.data.decode()}'

   assert "return" in resp_json, "Expected 'return' in response"
   assert resp_json["return"] == text_data[KEY], f"Expected return to be {text_data[KEY]}, but got {resp_json['return']}"


def test_update_text():
   resp = TEST_CLIENT.get(ep.TEXT_EP)
   resp_json = resp.get_json()
   for key, thing in resp_json.items():
       assert isinstance(key, str)
       assert len(key) > 0
       assert TITLE in thing
       assert TEXT in thing


def test_delete_text():
   # creating a text to make sure the text we are trying to delete, exists
   text_data ={ 
        KEY: "AnotherPage",
        TITLE: "Another Page",
        TEXT: "This is another journal to test deleting text."
    }
   delete_data ={ 
        KEY: "AnotherPage",
    }
    
   create_resp = TEST_CLIENT.put(ep.TEXT_EP, json=text_data)
   create_resp_json = create_resp.get_json()
   created_key = create_resp_json.get("return")
 
   assert created_key == text_data[KEY], f"Expected return to be {text_data[KEY]}, but got {create_resp_json['return']}"

   del_resp = TEST_CLIENT.delete(ep.TEXT_EP, json = delete_data)
   del_resp_json = del_resp.get_json()
   print(del_resp_json)

   assert "Deleted!" in del_resp_json.get("Message"), "Expected 'Deleted' in response"
   assert created_key in del_resp_json["return"], f"Expected deleted key to be {created_key} but got {del_resp_json['return']}"

   # verifying if deleted
   read_resp = TEST_CLIENT.get(ep.TEXT_EP)
   read_resp_json = read_resp.get_json()
   
   assert created_key not in read_resp_json, "Text still found after delete"