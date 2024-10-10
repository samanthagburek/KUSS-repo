import pytest

import data.people as ppl
import pytest


def test_read():
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person
    
def test_del_person():
    people = ppl.get_people()
    old_len = len(people)
    ppl.delete_person(ppl.DEL_EMAIL)
    people = ppl.get_people()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people

ADD_EMAIL = "john@who.org"
    
def test_create_person():
    people = ppl.get_people()
    assert ADD_EMAIL not in people
    ppl.create_person(ADD_EMAIL, "John Smith", "WHO")
    people = ppl.get_people()
    assert ADD_EMAIL in people
    ppl.delete_person(ADD_EMAIL)
    
def test_create_duplicate_person():
    with pytest.raises(ValueError):
        ppl.create_person(ppl.TEST_EMAIL, "Name doesn't matter", "Affiliation doesn't matter")
