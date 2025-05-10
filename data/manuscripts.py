import data.db_connect as dbc
import re
# testing purposes
# import db_connect as dbc
from bson.objectid import ObjectId
MANU_COLLECT = 'manu'

# fields
ID = '_id'
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
NEW_STATE = 'new_state'


REF_ID = 'referee@sample.com'
REF_EMAIL = 'referee_email'
REF_REPORT = 'referee_report'
REF_VERDICT = 'referee_verdict'


DISP_NAME = 'disp_name'
MANU_ID = '_id'

ACTION = 'action'

TEST_ID = 'fake_i'
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


VALID_STATES = {
    SUBMITTED: "Submitted",
    IN_REF_REV: "In Referee Review",
    AUTHOR_REVISIONS: "In Author Revisions",
    EDITOR_REVIEW: "In Editor Review",
    COPY_EDIT: "In Copy Edit",
    AUTHOR_REVIEW: "In Author Review",
    FORMATTING: "Formatting",
    PUBLISHED: "Published",
    REJECTED: "Rejected",
    WITHDRAWN: "Withdrawn",
}


SAMPLE_MANU = {
    TITLE: 'Short module import names in Python',
    AUTHOR: 'Eugene Callahan',
    REFEREES: [],
}

DEFAULT_EDITOR_EMAIL = "admin@gmail.com"
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
           text: str, abstract: str, referees: dict):

    # two manuscripts can have the same title
    # if title in read():
    #     raise ValueError(f'Manuscript already exists {title=}')
    if not is_valid_email(author_email):
        raise ValueError(f'Invalid email: {author_email}')
    if not is_valid_email(DEFAULT_EDITOR_EMAIL):
        raise ValueError(f'Invalid email: {DEFAULT_EDITOR_EMAIL}')

    newmanu = {TITLE: title, AUTHOR: author,
               AUTHOR_EMAIL: author_email, TEXT: text,
               ABSTRACT: abstract, EDITOR_EMAIL: DEFAULT_EDITOR_EMAIL,
               REFEREES: referees, STATE: SUBMITTED}
    result = dbc.create(MANU_COLLECT, newmanu)
    newmanu["_id"] = str(result.inserted_id)
    return newmanu


def delete(_id: str):
    return dbc.delete(MANU_COLLECT, {'_id': ObjectId(_id)})


def update(_id: str, title: str, author: str, author_email: str, text: str,
           abstract: str, editor_email: str):
    return dbc.update_doc(MANU_COLLECT, {'_id': ObjectId(_id)},
                                        {TITLE: title,
                                         AUTHOR: author,
                                         AUTHOR_EMAIL: author_email,
                                         TEXT: text,
                                         ABSTRACT: abstract,
                                         EDITOR_EMAIL: editor_email})
    # else:
    #     raise ValueError(f'Manuscript not found {title=}')


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    manuscripts = dbc.read(MANU_COLLECT, no_id=False)
    for manu in manuscripts:
        manu["_id"] = str(manu["_id"])
        # manu[STATE] = VALID_STATES.get(manu[STATE], manu[STATE])
    return manuscripts


def read_one(_id: str) -> dict:
    # return PERSON_DICT.get(email, None)
    manu = dbc.fetch_one(MANU_COLLECT, {'_id': ObjectId(_id)})
    if manu:
        manu["_id"] = str(manu["_id"])
        # manu[STATE] = VALID_STATES.get(manu[STATE], manu[STATE])
    return manu
    # print(f'{manu=}')
    # if manu:
    #     manu['_id'] = str(manu['_id'])
    # return manu


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

VALID_ACTIONS = {
    ACCEPT: "Accept",
    ASSIGN_REF: "Assign Referee",
    DELETE_REF: "Delete Referee",
    DONE: "Done",
    REJECT: "Reject",
    WITHDRAW: "Withdraw",
    SUBMIT_REVIEW: "Submit Review",
    ACCEPT_W_REVISIONS: "Accept With Revisions",
    EDITOR_MOV: "Editor Move",
}

VALID_VERDICTS = {
    'ACCEPT': 'Accept',
    'ACCWREV': 'Accept With Revisions',
    'REJECT': 'Reject',
}


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


# need to acc set the ref report and ref verdict
# in submit review and accept with revisions
def assign_ref(manu, referee: str, extra=None) -> str:
    refs = manu.get(REFEREES, {})
    refs[referee] = {
        REF_REPORT: "string",
        REF_VERDICT: "string",
    }
    result = dbc.update_doc(MANU_COLLECT, {"_id": ObjectId(manu['_id'])},
                            {'referees': refs})
    print(result)
    return IN_REF_REV

# def assign_ref(manu: dict, referee: str, extra=None) -> str:
#     dic = {referee: {REF_REPORT: "string", REF_VERDICT: "string",}}
#     manu[REFEREES][referee] = dic
#     return IN_REF_REV


# def delete_ref(manu: dict, referee: str) -> str:
#     if len(manu[REFEREES]) > 0:
#        result = dbc.delete(MANU_COLLECT, {"_id":
#                                   ObjectId(manu['_id'])})
#        print(result)
#    if len(manu[REFEREES]) > 0:
#        return IN_REF_REV
#   else:
#        return SUBMITTED


def delete_ref(manu: dict, referee: str) -> str:
    referees = manu.get(REFEREES, {})

    if referee in referees:
        referees.pop(referee)
        dbc.update_doc(MANU_COLLECT, {'_id': ObjectId(manu['_id'])},
                       {REFEREES: referees})

    if referees:
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
            FUNC: lambda **kwargs: submit_review(kwargs['manu'],
                                                 kwargs['referee'],
                                                 kwargs[REF_REPORT],
                                                 kwargs[REF_VERDICT]),
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
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REVIEW,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    AUTHOR_REVIEW: {
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    AUTHOR_REVISIONS: {
        DONE: {
            FUNC: lambda **kwargs: EDITOR_REVIEW,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    REJECTED: {
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    WITHDRAWN: {
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    PUBLISHED: {
        EDITOR_MOV: {
             FUNC: lambda **kwargs: editor_move(kwargs['new_state'])
        },
    },
    DONE: {
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return {code: VALID_ACTIONS.get(code, code) for code in valid_actions}


def handle_action(_id, curr_state, action, **kwargs) -> str:
    # kwargs['manu'] = SAMPLE_MANU
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')

    manu_doc = read_one(_id)
    if manu_doc:
        kwargs['manu'] = manu_doc
        state = STATE_TABLE[curr_state][action][FUNC](**kwargs)
        result = dbc.update_doc(MANU_COLLECT, {'_id': ObjectId(_id)},
                                {STATE: str(state)})
        print(f'result={result}, str_state={str(state)}')
        return state
    else:
        return f'Error {_id} is not a valid manuscript'


def handle_withdraw(_id, **kwargs) -> str:
    manu_doc = read_one(_id)
    if manu_doc:
        kwargs['manu'] = manu_doc
        state = COMMON_ACTIONS[WITHDRAW][FUNC](**kwargs)
        result = dbc.update_doc(MANU_COLLECT, {'_id': ObjectId(_id)},
                                {STATE: str(state)})
        print(f'result={result}, str_state={str(state)}')
        return state
    else:
        return f'Error {_id} is not a valid manuscript'


def submit_review(manu: dict, referee: str, report: str, verdict: str,
                  **kwargs) -> str:
    if referee not in manu[REFEREES]:
        raise ValueError(f"Referee {referee} not assigned to manuscript")

    manu[REFEREES][referee] = {
        REF_REPORT: report,
        REF_VERDICT: VALID_VERDICTS[verdict],
    }

    dbc.update_doc(MANU_COLLECT, {"_id": ObjectId(manu['_id'])},
                   {REFEREES: manu[REFEREES]})

    return IN_REF_REV


def get_verdicts() -> dict:
    return VALID_VERDICTS

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
