ACTION = 'action'
AUTHOR = 'author'
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = '_id'
REFEREE = 'referee'
REFEREES = 'referees'
TITLE = 'title'

TEST_ID = 'fake_id'
TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'


FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
}

# states:
AUTHOR_REVIEW = 'AUREVIEW'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'
AUTHOR_REVISIONS = 'AUREVISION'
EDITOR_REVIEW = 'EDREV'
FORMATTING = 'FOR'
PUBLISHED = 'PUB'

TEST_STATE = SUBMITTED


VALID_STATES = [
    AUTHOR_REVIEW,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    WITHDRAWN,
    AUTHOR_REVISIONS,
    EDITOR_REVIEW,
    FORMATTING,
    PUBLISHED,
]


SAMPLE_MANU = {
    TITLE: 'Short module import names in Python',
    AUTHOR: 'Eugene Callahan',
    REFEREES: [],
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
SUBMIT_REVIEW = 'SUBREV'
ACCEPT_W_REVISIONS = 'ACCWREV'
EDITOR_MOV = 'EDMOV'

# for testing:
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAW,
    SUBMIT_REVIEW,
    ACCEPT_W_REVISIONS,
    EDITOR_MOV
]


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def assign_ref(manu: dict, referee: str, extra=None) -> str:
    manu[REFEREES].append(referee)
    return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[REFEREES]) > 0:
        manu[REFEREES].remove(referee)
    if len(manu[REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


FUNC = 'f'

COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        SUBMIT_REVIEW: {
            FUNC: lambda **kwargs: IN_REF_REV,
        },
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        ACCEPT_W_REVISIONS: {
            FUNC: lambda **kwargs: AUTHOR_REVISIONS,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVIEW: {
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISIONS: {
        DONE: {
            FUNC: lambda **kwargs: EDITOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
        **COMMON_ACTIONS,
    },
    REJECTED: {
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        **COMMON_ACTIONS,
    },
    PUBLISHED: {
        **COMMON_ACTIONS,
    },

}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(manu_id, curr_state, action, **kwargs) -> str:
    kwargs['manu'] = SAMPLE_MANU
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)


def main():
    print(handle_action(TEST_ID, SUBMITTED, ASSIGN_REF, ref='Jack'))
    print(handle_action(TEST_ID, IN_REF_REV, ASSIGN_REF,
                        ref='Jill', extra='Extra!'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jill'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jack'))
    print(handle_action(TEST_ID, SUBMITTED, WITHDRAW))
    print(handle_action(TEST_ID, SUBMITTED, REJECT))


if __name__ == '__main__':
    main()
