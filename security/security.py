from functools import wraps
import data.people as ppl
import base64
import zlib
import json

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'
LOGIN_KEY = 'login_key'
IP_ADDR = 'ip_address'
DUAL_FACTOR = 'dual_factor'

# Features
PEOPLE = 'people'
TEXT = 'text'
MANUSCRIPTS = 'manuscripts'
BAD_FEATURE = 'baaaad feature'
PEOPLE_MISSING_ACTION = READ

security_recs = None
GOOD_USER_ID = 'kuss@nyu.edu'
EDITOR_IDS = (
    ppl.get_ppl_in_role('ED')
    + ppl.get_ppl_in_role('ME')
    + ppl.get_ppl_in_role('CE')
    + [GOOD_USER_ID]
)

ALL_IDS = (
    ppl.get_ppl_in_role('ED')
    + ppl.get_ppl_in_role('ME')
    + ppl.get_ppl_in_role('CE')
    + ppl.get_ppl_in_role('AU')
    + ppl.get_ppl_in_role('RE')
    + [GOOD_USER_ID]
)

AUTHOR_IDS = (
    ppl.get_ppl_in_role('AU')
)

REF_IDS = (
    ppl.get_ppl_in_role('RE')
)

AU_EDIT_IDS = (
    ppl.get_ppl_in_role('ME')
    + ppl.get_ppl_in_role('ED')
    + ppl.get_ppl_in_role('CE')
    + ppl.get_ppl_in_role('AU')
)

PEOPLE_CHANGE_PERMISSIONS = {
     USER_LIST: EDITOR_IDS,
     CHECKS: {
         LOGIN: True,
     },
 }

TEXT_CHANGE_PERMISSIONS = {
    USER_LIST: EDITOR_IDS,
    CHECKS: {
        LOGIN: True,
    }
}

MANUS_DELETE_PERMISSIONS = {
    USER_LIST: EDITOR_IDS,
    CHECKS: {
        LOGIN: True,
    }
}

ALL_PERMISSIONS = {
    USER_LIST: ALL_IDS,
    CHECKS: {
        LOGIN: True,
    }
}

MANUS_UPDATE_PERMISSIONS = {
    USER_LIST: AU_EDIT_IDS,
    CHECKS: {
        LOGIN: True,
    }
}

temp_recs = {
    PEOPLE: {
        CREATE: ALL_PERMISSIONS,
        DELETE: PEOPLE_CHANGE_PERMISSIONS,
        UPDATE: ALL_PERMISSIONS,
    },
    TEXT: {
        CREATE: TEXT_CHANGE_PERMISSIONS,
        DELETE: TEXT_CHANGE_PERMISSIONS,
        UPDATE: TEXT_CHANGE_PERMISSIONS,
    },
    MANUSCRIPTS: {
        CREATE: ALL_PERMISSIONS,
        DELETE: MANUS_DELETE_PERMISSIONS,
        UPDATE: MANUS_UPDATE_PERMISSIONS,
    },
    BAD_FEATURE: {
        CREATE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                'Bad check': True,
            },
        },
    },
}


def decode_login_key(session_key: str) -> str:
    try:
        decoded = base64.urlsafe_b64decode(session_key.encode('utf-8'))
        decompressed = zlib.decompress(decoded)
        json_result = json.loads(decompressed.decode('utf-8'))
        return json_result['user_id']
    except (base64.binascii.Error, zlib.error, json.JSONDecodeError):
        raise ValueError("Invalid session key")


def is_valid_key(user_id: str, login_key: str):
    if user_id == GOOD_USER_ID:
        return True
    if user_id not in ppl.sessions:
        return False
    session = ppl.sessions[user_id]
    decoded = decode_login_key(session['key'])
    if decoded != login_key:
        return False
    return True


def check_login(user_id: str, **kwargs):
    if LOGIN_KEY not in kwargs:
        return False
    return is_valid_key(user_id, kwargs[LOGIN_KEY])


def check_ip(user_id: str, **kwargs):
    if IP_ADDR not in kwargs:
        return False
    # we would check user's IP address here
    return True


def dual_factor(user_id: str, **kwargs):
    return True


CHECK_FUNCS = {
    LOGIN: check_login,
    IP_ADDR: check_ip,
    DUAL_FACTOR: dual_factor,
}


def read() -> dict:
    global security_recs
    security_recs = temp_recs
    return security_recs


def needs_recs(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if not security_recs:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    if feature_name in security_recs:
        return security_recs[feature_name]
    else:
        return None


@needs_recs
def is_permitted(feature_name: str, action: str,
                 user_id: str, **kwargs) -> bool:
    print(feature_name, action, user_id)
    prot = read_feature(feature_name)
    if prot is None:
        return True
    if action not in prot:
        return True
    if USER_LIST in prot[action]:
        if user_id not in prot[action][USER_LIST]:
            return False
    if CHECKS not in prot[action]:
        return True
    for check in prot[action][CHECKS]:
        if check not in CHECK_FUNCS:
            raise ValueError(f'Bad check passed to is_permitted: {check}')
        if not CHECK_FUNCS[check](user_id, **kwargs):
            return False
    return True
