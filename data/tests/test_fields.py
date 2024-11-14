TEMP_NAME = 'temp'
import data.fields as fld


def test_get_fields():
    fields = fld.get_fields()
    assert isinstance(fields, dict)
    assert len(fields) > 0
    assert isinstance(fields[fld.TITLE], dict)
    for key, value in fields[fld.TITLE].items():
        assert isinstance(key, str)
        assert isinstance(value, str)
