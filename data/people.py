"""
This module interfaces to our user data.
"""

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


def create(_id: str, name: str, aff: str):
    people = read()
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
    print(read())


if __name__ == '__main__':
    main()
