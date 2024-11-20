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
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'dbw1947@nyu.edu'
DEL_EMAIL = 'del@nyu.edu'

PERSON_DICT = {
    TEST_EMAIL: {
        NAME: 'David Bowie',
        ROLES: [rls.ED_CODE],
        AFFILIATION: 'Starman',
        EMAIL: TEST_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'Someone',
        ROLES: [rls.CE_CODE],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    }
}

CHAR_OR_DIGIT = '[A-Za-z0-9]'
VALID_CHARS = '[A-Za-z0-9_.]'

client = dbc.connect_db()
print(f'{client=}')


def is_valid_email(email: str) -> bool:
    return re.fullmatch(f"{VALID_CHARS}+@{CHAR_OR_DIGIT}+"
                        + "\\."
                        + f"{CHAR_OR_DIGIT}"
                        + "{2,3}", email)


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
                    role: str = None, roles: list = None) -> bool:
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if role:
        if not rls.is_valid(role):
            raise ValueError(f'Invalid role: {role}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def create(_id: str, name: str, aff: str, role: str):
    if _id in read():
        raise ValueError(f"Adding duplicate email {_id=}")
    if (is_valid_person(_id, name, aff, role)):
        roles = []
        if role:
            roles.append(role)
        # people = read()
        # people[_id]= {NAME: name, ROLES: roles, AFFILIATION: aff, EMAIL: _id}
        newperson = {NAME: name, ROLES: roles, AFFILIATION: aff, EMAIL: _id}
        dbc.create(PEOPLE_COLLECT, newperson)
        return _id


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = {}
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


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
    return dbc.update_doc(PEOPLE_COLLECT, {EMAIL: _id},
                          {NAME: name, AFFILIATION: aff,
                          ROLES: roles, EMAIL: _id})
    # return _id


def update_role(_id: str, role: str):
    person = read_one(_id)
    if person is None:
        raise ValueError(f'User not found {_id=}')
    people = read()
    if rls.is_valid(role):
        people[_id][ROLES].append(role)


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
