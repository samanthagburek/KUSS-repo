import random

import pytest

import data.manuscripts as mqry
import data.people as ppl 


def gen_random_not_valid_str() -> str:
    """
    That huge number is only important in being huge:
        any big number would do.
    """
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())


def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_is_not_valid_action():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_ID,
                           gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_ID,
                           mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           manu=mqry.SAMPLE_MANU)


@pytest.mark.skip(reason="Need to fix for db")
def test_handle_action_valid_return():

    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{action=}')
            if action == mqry.DONE:
                continue
            if action == mqry.EDITOR_MOV:
                  new_state = mqry.handle_action(
                    mqry.TEST_ID, state, action, manu=mqry.SAMPLE_MANU, new_state=random.choice(mqry.get_states())
                )
                  print(new_state)
            else:
                new_state = mqry.handle_action(mqry.TEST_ID,
                                                state,
                                                action,
                                                manu=mqry.SAMPLE_MANU,
                                                referee='Some ref')
            print(f'{new_state=}')
            assert mqry.is_valid_state(new_state)


@pytest.mark.skip(reason="Need to fix for db")
def test_reject():
    new_state = mqry.handle_action(mqry.TEST_ID, mqry.SUBMITTED, mqry.REJECT, manu=mqry.SAMPLE_MANU)
    assert new_state == mqry.REJECTED


@pytest.mark.skip(reason="Need to fix for db")
def test_editor_move():
    if mqry.EDITOR_MOV in mqry.VALID_ACTIONS:
        for state in mqry.get_states():
            forced_state = random.choice(mqry.get_states())
            new_state = mqry.handle_action(mqry.TEST_ID, 
                                           state, 
                                           mqry.EDITOR_MOV, 
                                           manu=mqry.SAMPLE_MANU, 
                                           new_state=forced_state)
            assert new_state == forced_state

@pytest.mark.skip(reason="Need to fix for db")
def test_withdraw_any_state():
    print(mqry.create(mqry.TEST_ID, "David", ppl.TEST_EMAIL, "Test", "Test",
                              ppl.TEST_EMAIL, ppl.TEST_EMAIL))
    for state in mqry.get_states():
        new_state = mqry.handle_action(mqry.TEST_ID, state, mqry.WITHDRAW, manu=mqry.SAMPLE_MANU)
        assert new_state == mqry.WITHDRAWN

@pytest.mark.skip(reason="Need to fix for db")
def test_done_transitions():
    transitions = [
        (mqry.AUTHOR_REVISIONS, mqry.EDITOR_REVIEW),
        (mqry.COPY_EDIT, mqry.AUTHOR_REVIEW),
        (mqry.AUTHOR_REVIEW, mqry.FORMATTING),
        (mqry.FORMATTING, mqry.PUBLISHED),
    ]
    for curr, expected in transitions:
        new_state = mqry.handle_action(mqry.TEST_ID, curr, mqry.DONE, manu=mqry.SAMPLE_MANU)
        assert new_state == expected

TEMP_EMAIL = 'temp_person@temp.org'
NO_AT = 'bademail'
NO_NAME = '@bademail'
NO_DOMAIN = 'bademail@'
NO_SUB_DOMAIN = 'bademail@com'
DOMAIN_TOO_SHORT = 'bademail@nyu.e'
DOMAIN_TOO_LONG = 'bademail@nyu.eedduu'
TEMP_EMAIL2 = 'not_real@temp.org'

def test_is_valid_email_no_at():
    assert not mqry.is_valid_email(NO_AT)


def test_is_valid_no_name():
    assert not mqry.is_valid_email(NO_NAME)


def test_is_valid_no_domain():
    assert not mqry.is_valid_email(NO_DOMAIN)

def test_is_valid_no_sub_domain():
    assert not mqry.is_valid_email(NO_SUB_DOMAIN)


def test_is_valid_email_domain_too_short():
    assert not mqry.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not mqry.is_valid_email(DOMAIN_TOO_LONG)

def test_is_valid_email():
    assert mqry.is_valid_email('un2021@nyu.edu')