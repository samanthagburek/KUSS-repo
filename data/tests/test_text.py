import pytest

import data.text as txt

TESTKEY = "TestPage"
TESTTITLE = "Test Title"
TESTTEXT = "Test Text"

def test_create():
    txt.create(TESTKEY, TESTTITLE, TESTTEXT)
    assert len(txt.read_one(TESTKEY)) > 0


def test_read():
    text = txt.read()
    assert isinstance(text, dict)
    assert len(text) > 0
    for _id, thing in text.items():
        assert isinstance(_id, str)
        assert txt.TITLE in thing


def test_read_one():
    assert len(txt.read_one(TESTKEY)) > 0


def test_read_one_not_found():
    assert txt.read_one('Not a page key') == None


def test_update():
    text = txt.read()
    assert TESTKEY in text
    txt.update(TESTKEY, "Test Title V2", "The update function worked!")
    text = txt.read()
    thetext = text[TESTKEY]
    assert thetext[txt.TITLE] == "Test Title V2"
    assert thetext[txt.TEXT] == "The update function worked!"


def test_delete():
    text = txt.read()
    old_len = len(text)
    txt.delete(TESTKEY)
    text = txt.read()
    assert len(text) < old_len
    assert TESTKEY not in text