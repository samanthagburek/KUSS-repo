import data.db_connect as dbc
import re
# testing purposes
# import db_connect as dbc

MANU_COLLECT = 'manu'

# fields
TITLE = 'title'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
CURR_STATE = 'curr_state'
TEXT = 'text'
ABSTRACT = 'abstract'
EDITOR_EMAIL = 'editor_email'
REFEREES = 'referees'
REFEREE = 'referee'
STATE = 'state'


REF_ID = 'referee@sample.com'
REF_EMAIL = 'referee_email'
REF_REPORT = 'referee_report'
REF_VERDICT = 'referee_verdict'


DISP_NAME = 'disp_name'
MANU_ID = '_id'

ACTION = 'action'

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

client = dbc.connect_db()
print(f'{client=}')

VALID_CHARS = '[A-Za-z0-9._%+-]'
DOMAIN_CHARS = '[A-Za-z0-9-]'
TLD_CHARS = '[A-Za-z]{2,3}'


def is_valid_email(email: str) -> bool:
    return re.fullmatch(f"{VALID_CHARS}+@"
                        + f"{DOMAIN_CHARS}+(\\.{DOMAIN_CHARS}+)*"
                        + f"\\.{TLD_CHARS}", email)


def create(title: str, author: str, author_email: str,
           text: str, abstract: str, editor_email: str, referees: dict):
    if title in read():
        raise ValueError(f'Manuscript already exists {title=}')
    if not is_valid_email(author_email):
        raise ValueError(f'Invalid email: {author_email}')
    if not is_valid_email(editor_email):
        raise ValueError(f'Invalid email: {editor_email}')

    newmanu = {TITLE: title, AUTHOR: author,
               AUTHOR_EMAIL: author_email, TEXT: text,
               ABSTRACT: abstract, EDITOR_EMAIL: editor_email,
               REFEREES: referees, STATE: SUBMITTED}
    dbc.create(MANU_COLLECT, newmanu)
    return title


def delete(title: str):
    return dbc.delete(MANU_COLLECT, {TITLE: title})


def update(title: str, author: str, author_email: str, text: str,
           abstract: str, editor_email: str, referees: dict):
    if title in read():
        return dbc.update_doc(MANU_COLLECT, {TITLE: title},
                                            {TITLE: title, AUTHOR: author,
                                             AUTHOR_EMAIL: author_email,
                                             TEXT: text,
                                             ABSTRACT: abstract,
                                             EDITOR_EMAIL: editor_email,
                                             REFEREES: referees})
    else:
        raise ValueError(f'Manuscript not found {title=}')


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = dbc.read_dict(MANU_COLLECT, TITLE)
    return text


def read_one(title: str) -> dict:
    # return PERSON_DICT.get(email, None)
    manu = dbc.fetch_one(MANU_COLLECT, {TITLE: title})
    print(f'{manu=}')
    return manu


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


# need to acc set the ref report and ref verdict
# in submit review and accept with revisions
def assign_ref(manu, referee: str, extra=None) -> str:
    dic = {referee: {REF_REPORT: "string", REF_VERDICT: "string", }}
    result = dbc.update_doc(MANU_COLLECT, {TITLE: manu[TITLE]},
                            {f'referees.{referee}': dic})
    print(result)
    return IN_REF_REV

# def assign_ref(manu: dict, referee: str, extra=None) -> str:
#     dic = {referee: {REF_REPORT: "string", REF_VERDICT: "string",}}
#     manu[REFEREES][referee] = dic
#     return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[REFEREES]) > 0:
        result = dbc.remove_nested(MANU_COLLECT, {TITLE: manu[TITLE]},
                                   REFEREES, referee)
        print(result)
    if len(manu[REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


def editor_move(new_state: str) -> str:
    if new_state not in VALID_STATES:
        raise ValueError(f'Invalid state: {new_state}')
    return new_state


FUNC = 'f'

COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda **kwargs: assign_ref(kwargs['manu'],
                                              kwargs['referee']),
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: lambda **kwargs: assign_ref(kwargs['manu'],
                                              kwargs['referee']),
        },
        DELETE_REF: {
            FUNC: lambda **kwargs: delete_ref(kwargs['manu'],
                                              kwargs['referee']),
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
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REVIEW,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVIEW: {
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISIONS: {
        DONE: {
            FUNC: lambda **kwargs: EDITOR_REVIEW,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    REJECTED: {
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
    PUBLISHED: {
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
        **COMMON_ACTIONS,
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(title, curr_state, action, **kwargs) -> str:
    # kwargs['manu'] = SAMPLE_MANU
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    if title in read():
        kwargs['manu'] = read_one(title)
        state = str(STATE_TABLE[curr_state][action][FUNC](**kwargs))
        result = dbc.update_doc(MANU_COLLECT, {TITLE: title},
                                {STATE: state})
        print(result)
        return STATE_TABLE[curr_state][action][FUNC](**kwargs)

# def main():
#    print(handle_action('name', IN_REF_REV, DELETE_REF, referee='string'))
#    print(handle_action(TEST_ID, IN_REF_REV, ASSIGN_REF,
#                        ref='Jill', extra='Extra!'))
#    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
#                        ref='Jill'))
#    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
#                        ref='Jack'))
#    print(handle_action(TEST_ID, SUBMITTED, WITHDRAW))

# if __name__ == '__main__':
#      main()
