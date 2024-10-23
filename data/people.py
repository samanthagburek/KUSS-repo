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


def is_valid_email(email: str) -> bool:
    return re.match(f"{CHAR_OR_DIGIT}.*@{CHAR_OR_DIGIT}.*", email)


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    people = PERSON_DICT
    return people


def delete(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def create(_id: str, name: str, aff: str, role: str):
    people = read()
    if not is_valid_email(_id):
        raise ValueError(f'Invalid email {_id=}')
    if _id not in people:
        people[_id] = {NAME: name, ROLES: [], AFFILIATION: aff, EMAIL: _id}
        return _id
    else:
        raise ValueError(f'Adding duplicate {_id=}')


def update(_id: str, name: str, aff: str):
    people = read()
    if _id in people:
        people[_id][NAME] = name
        people[_id][AFFILIATION] = aff
        return _id
    else:
        raise ValueError(f'User not found {_id=}')


def main():
    create("johnnyu.edu", "x", "x")
    print(read())


if __name__ == '__main__':
    main()
