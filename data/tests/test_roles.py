import data.roles as rls
import pytest

TEMP_ROLE = "TEMP"

@pytest.fixture(scope='function')
def temp_role():
    ret = rls.create_role(TEMP_ROLE, 'TEMP')
    yield ret
    rls.delete_role(ret)

def test_get_roles():
    roles = rls.get_roles()
    assert isinstance(roles, dict)
    assert len(roles) > 0
    for code, role in roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)

ADD_ROLE = "TST"

def test_add_roles():
    roles = rls.get_roles()
    assert ADD_ROLE not in roles
    rls.create_role(ADD_ROLE, "Test")
    roles = rls.get_roles()
    assert ADD_ROLE in roles
    rls.delete_role(ADD_ROLE)

def test_update_roles(temp_role):
    roles = rls.get_roles()
    rls.update_role(temp_role, "TestUpdate")
    roles = rls.get_roles()
    assert roles[temp_role] == "TestUpdate"

def test_double_makemasthead(temp_role):
    rls.make_masthead_role(temp_role)
    with pytest.raises(ValueError):
        rls.make_masthead_role(temp_role)

def test_double_makenormal(temp_role):
    rls.make_normal_role(temp_role)
    with pytest.raises(ValueError):
        rls.make_normal_role(temp_role)

def test_get_masthead_roles():
    mh_roles = rls.get_masthead_roles()
    assert isinstance(mh_roles, dict)

def test_makemasthead(temp_role):
    rls.make_masthead_role(temp_role)
    mh_roles = rls.get_masthead_roles()
    assert temp_role in mh_roles
    
def test_is_valid():
    assert rls.is_valid(rls.TEST_CODE)

def test_get_role_codes():
    codes = rls.get_role_codes()
    assert isinstance(codes, list)
    for code in codes:
        assert isinstance(code, str)