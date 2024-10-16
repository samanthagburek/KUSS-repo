import pytest

import data.text as txt


def test_read():
    text = txt.read()
    assert isinstance(text, dict)
    assert len(text) > 0
    for _id, thing in text.items():
        assert isinstance(_id, str)
        assert txt.TITLE in thing
