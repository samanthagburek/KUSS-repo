"""
This module interfaces to our user data.
"""
import re
import data.roles as rls
import data.db_connect as dbc

PEOPLE_COLLECT = 'people'


MIN_USER_NAME_LEN = 2
# fields
NAME = 'name'
PASSWORD = 'password'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'dbw1947@nyu.edu'
DEL_EMAIL = 'del@nyu.edu'
TEST_ROLE_EMAIL = 'rol@gmail.com'
LOGIN_FAIL = ''

PERSON_DICT = {
    TEST_EMAIL: {
        NAME: 'David Bowie',
        PASSWORD: '',
        ROLES: [rls.ED_CODE],
        AFFILIATION: 'Starman',
        EMAIL: TEST_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'Someone',
        PASSWORD: '',
        ROLES: [rls.CE_CODE],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    },
    TEST_ROLE_EMAIL: {
        NAME: 'Someone',
        PASSWORD: '',
        ROLES: [rls.AUTHOR_CODE],
        AFFILIATION: 'INC',
        EMAIL: TEST_ROLE_EMAIL,
    },
    LOGIN_FAIL: {
        NAME: '',
        PASSWORD: '',
        ROLES: [],
        AFFILIATION: '',
        EMAIL: LOGIN_FAIL,
    }
}


client = dbc.connect_db()
print(f'{client=}')


VALID_CHARS = '[A-Za-z0-9._%+-]'
DOMAIN_CHARS = '[A-Za-z0-9-]'
TLD_CHARS = '[A-Za-z]{2,3}'


def is_valid_email(email: str) -> bool:
    return re.fullmatch(f"{VALID_CHARS}+@"
                        + f"{DOMAIN_CHARS}+(\\.{DOMAIN_CHARS}+)*"
                        + f"\\.{TLD_CHARS}", email)


def read() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    # print("read() has been called")
    # return PERSON_DICT
    people = dbc.read_dict(PEOPLE_COLLECT, EMAIL)
    print(f'{people=}')
    return people


# Get single person by id, or return None if id doesn't exist
def read_one(email: str) -> dict:
    # return PERSON_DICT.get(email, None)
    person = dbc.fetch_one(PEOPLE_COLLECT, {EMAIL: email})
    print(f'{person=}')
    return person


def try_login(email: str, password: str) -> dict:
    # return PERSON_DICT.get(email, None)
    person = dbc.fetch_one(PEOPLE_COLLECT, {EMAIL: email})
    if person is None:
        return None
    if person[PASSWORD] == password:
        return person
    else:
        return None


def delete(_id):
    """ people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None """
    print(f'{EMAIL=}, {_id=}')
    return dbc.delete(PEOPLE_COLLECT, {EMAIL: _id})


def is_valid_person(email: str, name: str, affiliation: str,
                    roles: list = None) -> bool:
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def create(_id: str, name: str, password: str, aff: str, roles: list):
    if _id in read():
        raise ValueError(f"Adding duplicate email {_id=}")
    if (is_valid_person(_id, name, aff, roles)):
        # people = read()
        # people[_id]= {NAME: name, ROLES: roles, AFFILIATION: aff, EMAIL: _id}
        newperson = {NAME: name, PASSWORD: password,
                     ROLES: roles, AFFILIATION: aff, EMAIL: _id}
        dbc.create(PEOPLE_COLLECT, newperson)
        return _id


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                rec['role'] = text
                people_w_role.append(rec)
        masthead[text] = people_w_role
    print(f'{masthead=}')
    return masthead


def get_ppl_in_role(role: str) -> dict:
    curr_ppl = []
    people = read()
    print(people)
    for _id, p in people.items():
        if has_role(p, role):
            curr_ppl.append(p['email'])
    print(f'{curr_ppl=}')
    return curr_ppl


'''update takes in a list for roles, but should it take in
one role then call update_role'''


def update(_id: str, name: str, aff: str, roles: list):
    person = read_one(_id)
    if person is None:
        raise ValueError(f'User not found {_id=}')
    if len(name) < MIN_USER_NAME_LEN:
        raise ValueError('Name is too short.')
    # PERSON_DICT[_id] = {NAME: name, AFFILIATION: aff,
    #                     EMAIL: _id, ROLES: roles}
    ret = dbc.update_doc(PEOPLE_COLLECT, {EMAIL: _id},
                         {NAME: name, AFFILIATION: aff,
                         ROLES: roles,
                         EMAIL: _id})
    return ret.raw_result


def update_role(_id: str, role: str):
    person = read_one(_id)
    if person is None:
        raise ValueError(f'User not found {_id=}')
    if rls.is_valid(role):
        if has_role(person, role):
            raise ValueError(f'User {_id=} already has {role=}')
        ret = dbc.update_array(PEOPLE_COLLECT, {EMAIL: _id}, ROLES, role)
        print(ret.raw_result)
        return ret.raw_result


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES):
        return True
    return False


MH_FIELDS = [NAME, AFFILIATION]


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in MH_FIELDS:
        mh_rec[field] = person.get(field, '')
    return mh_rec


def main():
    create("johnnyu.edu", "x", "x")
    print(read())


if __name__ == '__main__':
    main()
