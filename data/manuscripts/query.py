# states:
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
TEST_STATE = SUBMITTED
VALID_STATES = [
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
]
def get_states() -> list:
    return VALID_STATES
def is_valid_state(state: str) -> bool:
    return state in VALID_STATES

# actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'
# for testing:
TEST_ACTION = ACCEPT
VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
]
def get_actions() -> list:
    return VALID_ACTIONS
def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS

def handle_action(current_state: str, action: str) -> str:
    if not is_valid_state(current_state):
        raise ValueError(f'Invalid state: {current_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    new_state = current_state
    if current_state == SUBMITTED:
        if action == ASSIGN_REF:
            new_state = IN_REF_REV
        elif action == REJECT:
            new_state = REJECTED
    elif current_state == IN_REF_REV:
        if action == ACCEPT:
            new_state = COPY_EDIT
        elif action == REJECT:
            new_state = REJECTED
    return new_state