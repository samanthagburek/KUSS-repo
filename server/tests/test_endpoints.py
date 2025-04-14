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

from data.people import NAME, AFFILIATION, EMAIL, ROLES, TEST_ROLE_EMAIL
from data.text import KEY, TITLE, TEXT
from data.roles import TEST_CODE, MH_ROLES, CODE
import data.manuscripts as manu

import server.endpoints as ep
PEOPLE_LOC = 'data.people.'

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

# @pytest.mark.skip('Skipping b/c test is incomplete')
# def test_update_people():
#    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
#    resp_json = resp.get_json()
#    for _id, person in resp_json.items():
#        assert isinstance(_id, str)
#        assert len(_id) > 0
#        assert NAME in person
#        assert AFFILIATION in person
#        assert EMAIL in person


def test_create_people():
   person_data ={
        EMAIL: "john@who.org",
        NAME: "John Smith",
        AFFILIATION: "WHO",
        ROLES: [TEST_CODE]
   }

   resp = TEST_CLIENT.put(ep.PEOPLE_EP, json=person_data)
   resp_json = resp.get_json()
   assert resp_json is not None, f'Expected JSON response, but got None. Response text: {resp.data.decode()}'

   assert "return" in resp_json, "Expected 'return' in response"
   assert resp_json["return"] == person_data[EMAIL], f"Expected return to be {person_data[EMAIL]}, but got {resp_json['return']}"


def test_update_people():
   
   person_data ={
       EMAIL: "john@who.org",
       NAME: "Jane Smith",
       AFFILIATION: "WHO",
       ROLES: [TEST_CODE]
   }
   resp = TEST_CLIENT.patch(ep.PEOPLE_EP, json=person_data)
   resp_json = resp.get_json()
   print(resp_json)
   assert resp_json is not None, f'Expected JSON response, but got None. Response text: {resp.data.decode()}'
   assert "Person updated!" in resp_json['Message'], "Expected 'Person updated!' in response"
   #assert resp_json['return']['nModified'] > 0


def test_update_role():
   role_data ={ 
        CODE: 'CE',
    }
   resp = TEST_CLIENT.patch(f'{ep.PEOPLE_EP}/john@who.org/fake_user', json = role_data)
   resp_json = resp.get_json()
   print(resp_json)
   assert resp_json is not None, f'Expected JSON response, but got None. Response text: {resp.data.decode()}'
   assert "Person role updated!" in resp_json['Message'], f"Expected 'Person role updated!' in response"
   assert resp_json['return']['nModified'] > 0


def test_delete_people():
   '''
   # creating a person to make sure the person we are trying to delete, exists
   person_data ={
        EMAIL: "jane@you.org",
        NAME: "Jane Street",
        AFFILIATION: "YOU",
        ROLES: TEST_CODE
    }

   create_resp = TEST_CLIENT.put(ep.PEOPLE_EP, json=person_data)
   create_resp_json = create_resp.get_json()
   created_email = create_resp_json.get("return")
 
   assert created_email == person_data[EMAIL], f"Expected return to be {person_data[EMAIL]}, but got {create_resp_json['return']}"
   '''
   person_data_email ={
        EMAIL: "john@who.org",
   }
   del_resp = TEST_CLIENT.delete(ep.PEOPLE_EP, json=person_data_email)
  
   del_resp_json = del_resp.get_json()
   print(del_resp_json)
   
   assert "Deleted" in del_resp_json.get("Message"), f"Expected 'Deleted' in response, but got {del_resp_json['Message']}"
   #assert created_email in del_resp_json["return"] == created_email, f"Expected deleted ID to be {created_email} but got {del_resp_json['return']}"
   assert del_resp_json["return"] > 0, f"Expected deleted count > 0, but got {del_resp_json['return']}"

   # verifying if deleted
   read_resp = TEST_CLIENT.get(ep.PEOPLE_EP)
   read_resp_json = read_resp.get_json()
   
   assert person_data_email[EMAIL] not in read_resp_json, "Person still found after delete"


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
   print(resp_json)
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
   delete_data ={ 
        KEY: "CreatePage",
    }

   del_resp = TEST_CLIENT.delete(ep.TEXT_EP, json = delete_data)
   del_resp_json = del_resp.get_json()
   print(del_resp_json)

   assert "Deleted!" in del_resp_json.get("Message"), "Expected 'Deleted' in response"

   assert del_resp_json["return"] > 0, f"Expected deleted count > 0, but got {del_resp_json['return']}"

   # verifying if deleted
   read_resp = TEST_CLIENT.get(ep.TEXT_EP)
   read_resp_json = read_resp.get_json()
   print("AAAAAAAAAHHHHHHHHHHH")
   print(read_resp_json)
   assert delete_data[KEY] not in read_resp_json, "Text still found after delete"

@patch('data.text.read', autospec=True,
       return_value={'name': {TITLE: 'This title', TEXT: 'This text'}})
def test_get_text(mock_read):
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for key, thing in resp_json.items():
        assert isinstance(key, str)
        assert TITLE in thing
        assert TEXT in thing

@patch('data.manuscripts.handle_action', autospec=True,
       return_value='SOME STRING')
def test_handle_action(mock_read):
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/receive_action',
                           json={
                               manu.MANU_ID: 'some id',
                               manu.CURR_STATE: 'some state',
                               manu.ACTION: 'some action',
                           })
    assert resp.status_code == OK

def test_get_roles():
    resp = TEST_CLIENT.get(ep.ROLES_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for code, thing in resp_json.items():
        assert isinstance(code, str)
        assert isinstance(thing, str)

@patch(PEOPLE_LOC + 'read_one', autospec=True,
       return_value={NAME: 'Joe Schmoe'})
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id/fake_user')
    assert resp.status_code == OK

@patch(PEOPLE_LOC + 'read_one', autospec=True, return_value=None)
def test_read_one_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id/fake_user')
    assert resp.status_code == NOT_FOUND