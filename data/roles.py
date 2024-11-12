"""
This modules manages person roles for a journal.
"""
from copy import deepcopy

AUTHOR_CODE = 'AU'
TEST_CODE = AUTHOR_CODE
ED_CODE = 'ED'
ME_CODE = 'ME'
CE_CODE = 'CE'
RE_CODE = 'RE'

ROLES = {
    AUTHOR_CODE: 'Author',
    ED_CODE: 'Editor',
    ME_CODE: 'Managing Editor',
    CE_CODE: 'Consulting Editor',
    RE_CODE: 'Referee',
}

MH_ROLES = [CE_CODE, ED_CODE, ME_CODE]


def get_roles() -> dict:
    return deepcopy(ROLES)


def create_role(code: str, name: str) -> str:
    if is_valid(code):
        raise ValueError(f"Adding duplicate role {code=}")
    ROLES[code] = name
    return code


def update_role(code: str, name: str) -> str:
    if not is_valid(code):
        raise ValueError(f"Role does not exist {code=}")
    ROLES[code] = name
    return code


def delete_role(code: str) -> str:
    if not is_valid(code):
        raise ValueError(f"Role does not exist {code=}")
    del ROLES[code]
    return code


def get_masthead_roles() -> dict:
    mh_roles = get_roles()
    del_mh_roles = []
    for role in mh_roles:
        if role not in MH_ROLES:
            del_mh_roles.append(role)
    for del_role in del_mh_roles:
        del mh_roles[del_role]
    return mh_roles


def make_masthead_role(code: str) -> str:
    if not is_valid(code):
        raise ValueError(f"Role does not exist {code=}")
    if code in MH_ROLES:
        raise ValueError(f"Role already masthead {code=}")
    MH_ROLES.append(code)


def make_normal_role(code: str) -> str:
    if not is_valid(code):
        raise ValueError(f"Role does not exist {code=}")
    if code not in MH_ROLES:
        raise ValueError(f"Role already normal {code=}")
    MH_ROLES.remove(code)


def get_role_codes() -> list:
    return list(ROLES.keys())


def is_valid(code: str) -> bool:
    return code in ROLES


def main():
    print(get_masthead_roles())


if __name__ == '__main__':
    main()
