import pytest

import data.people as ppl
import pytest


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
    ppl.create(ADD_EMAIL, "John Smith", "WHO")
    people = ppl.read()
    assert ADD_EMAIL in people
    ppl.delete(ADD_EMAIL)
    
def test_create_duplicate():
    with pytest.raises(ValueError):
        ppl.create(ppl.TEST_EMAIL, "Name doesn't matter", "Affiliation doesn't matter")
