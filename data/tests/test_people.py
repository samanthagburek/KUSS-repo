import pytest

import data.people as ppl
from data.roles import TEST_CODE

TEMP_EMAIL = 'temp_person@temp.org'
NO_AT = 'bademail'
NO_NAME = '@bademail'
NO_DOMAIN = 'bademail@'
NO_SUB_DOMAIN = 'bademail@com'
DOMAIN_TOO_SHORT = 'bademail@nyu.e'
DOMAIN_TOO_LONG = 'bademail@nyu.eedduu'

@pytest.fixture(scope='function')
def temp_person():
    ret = ppl.create(TEMP_EMAIL, 'Joe Smith', 'NYU', TEST_CODE)
    yield ret
    ppl.delete(ret)

def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person
    
def test_delete():
    people = ppl.read()
    old_len = len(people)
    ppl.delete(ppl.DEL_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people

ADD_EMAIL = "john@who.org"
    
def test_create():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create(ADD_EMAIL, "John Smith", "WHO", TEST_CODE)
    people = ppl.read()
    assert ADD_EMAIL in people
    ppl.delete(ADD_EMAIL)


TEST_EMAIL = "dbw1947@nyu.edu"

def test_update():
    people = ppl.read()
    assert TEST_EMAIL in people
    ppl.update(TEST_EMAIL, "Kid Rock", "WHO", "singer")
    people = ppl.read()
    person = people[TEST_EMAIL]
    assert person[ppl.NAME] is "Kid Rock"
    assert person[ppl.AFFILIATION] is "WHO"
    ppl.update(TEST_EMAIL, "David Bowie", "Starman", "singer")
    
def test_create_duplicate():
    with pytest.raises(ValueError):
        ppl.create(ppl.TEST_EMAIL, "Name doesn't matter", "Affiliation doesn't matter", TEST_CODE)

def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)


def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)

def test_is_valid_no_sub_domain():
    assert not ppl.is_valid_email(NO_SUB_DOMAIN)


def test_is_valid_email_domain_too_short():
    assert not ppl.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(DOMAIN_TOO_LONG)

def test_is_valid_email():
    assert ppl.is_valid_email('un2021@nyu.edu')

def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)

def test_read_one(temp_person):
    assert ppl.read_one(temp_person) is not None

def test_read_one_not_there():
    assert ppl.read_one('Not an existing email!') is None