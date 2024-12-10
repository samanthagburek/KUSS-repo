import data.manuscripts.fields as flds
# states:
AUTHOR_REV = 'AUR'  # author review
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
FORMATTING = 'FOR'
PUBLISHED = 'PUB'
WITHDRAWN = 'WIT'

TEST_STATE = SUBMITTED
VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    WITHDRAWN,
    FORMATTING,
]

SAMPLE_MANU = {
    flds.TITLE: 'Short module import names in Python',
    flds.AUTHOR: 'Kuss Endname',
    flds.REFEREES: [],
}


def get_states() -> list:
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


# actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'
# for testing:
TEST_ACTION = ACCEPT
VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAWN,
]
FUNC = 'f'


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS

def assign_ref(manu: dict, ref: str, extra=None) -> str:
    manu[flds.REFEREES].append(ref)
    return IN_REF_REV
    
def delete_ref(manu: dict, ref: str) -> str:
    if len(manu[flds.REFEREES]) > 0:
        manu[flds.REFEREES].remove(ref)
    if len(manu[flds.REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda m: IN_REF_REV,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda m: AUTHOR_REV,
        },
    },
    AUTHOR_REV: {
        DONE: {
            FUNC: lambda m: FORMATTING,
        },
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda m: PUBLISHED,
        },
    },
    PUBLISHED: {},
    REJECTED: {},

}


def get_valid_actions_by_state(state: str) -> list:
    return STATE_TABLE[state].keys()


def handle_action(current_state: str, action: str, manuscript: str) -> str:
    if current_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {current_state}')
    if action not in STATE_TABLE[current_state]:
        raise ValueError(f'{action} not available in {current_state}')
    return STATE_TABLE[current_state][action][FUNC](manuscript)

def main():
    print(handle_action(SUBMITTED, ASSIGN_REF, SAMPLE_MANU))
    print(handle_action(SUBMITTED, REJECT, SAMPLE_MANU))