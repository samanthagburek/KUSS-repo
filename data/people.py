"""
This module interfaces to our user data.
"""
import re

import data.roles as rls

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
        ROLES: [],
        AFFILIATION: 'Starman',
        EMAIL: TEST_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'Someone',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    }
}

CHAR_OR_DIGIT = '[A-Za-z0-9]'
VALID_CHARS = '[A-Za-z0-9_.]'


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
    people = PERSON_DICT
    return people


def read_one(email: str) -> dict:
    return PERSON_DICT.get(email)


def delete(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


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
    if _id in PERSON_DICT:
        raise ValueError(f"Adding duplicate email {_id=}")
    if (is_valid_person(_id, name, aff, role)):
        roles = []
        if role:
            roles.append(role)
        people = read()
        people[_id] = {NAME: name, ROLES: roles, AFFILIATION: aff, EMAIL: _id}
        return _id


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = {}
        for person in read():
            pass
        masthead[text] = people_w_role
    return masthead


def update(_id: str, name: str, aff: str, roles: list):
    people = read()
    if _id not in people:
        raise ValueError(f'User not found {_id=}')
    PERSON_DICT[_id] = {NAME: name, AFFILIATION: aff,
                        EMAIL: _id, ROLES: roles}
    return _id


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES):
        return True
    return False


def main():
    create("johnnyu.edu", "x", "x")
    print(read())


if __name__ == '__main__':
    main()
