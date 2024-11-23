import pytest

import data.text as txt


def test_read():
    pass
    '''text = txt.read()
    assert isinstance(text, dict)
    assert len(text) > 0
    for _id, thing in text.items():
        assert isinstance(_id, str)
        assert txt.TITLE in thing'''
    
TESTKEY = "TestPage"
TESTTITLE = "Test Title"
TESTTEXT = "Test Text"

def test_create():
    pass
    # txt.create(TESTKEY, TESTTITLE, TESTTEXT)
    # assert len(txt.read_one(TESTKEY)) > 0


def test_read_one():
    pass
    # assert len(txt.read_one(txt.TEST_KEY)) > 0


def test_read_one_not_found():
    pass
    # assert txt.read_one('Not a page key') == {}


def test_update():
    pass
    '''text = txt.read()
    assert TESTKEY in text
    txt.update(TESTKEY, "Test Title V2", "The update function worked!")
    text = txt.read()
    thetext = text[TESTKEY]
    assert thetext[txt.TITLE] is "Test Title V2"
    assert thetext[txt.TEXT] is "The update function worked!"'''


def test_delete():
    pass
    '''text = txt.read()
    old_len = len(text)
    txt.delete(txt.DEL_KEY)
    text = txt.read()
    assert len(text) < old_len
    assert txt.DEL_KEY not in text'''