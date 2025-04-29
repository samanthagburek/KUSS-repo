"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields  # Namespace
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.people as ppl
import data.text as txt
import data.manuscripts as manu
import data.roles as rls
import security.security as sec

import logging
import os
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # Only log errors or worse

if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = logging.FileHandler('logs/error.log')
file_handler.setLevel(logging.ERROR)  # This ensures only errors go in the file
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
)
file_handler.setFormatter(formatter)
# Add handler to your specific logger
logger.addHandler(file_handler)

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
MESSAGE = 'Message'
TITLE_EP = '/title'
TITLE_RESP = 'Title: '
TITLE = 'The Journal of the KUSS Project'
EDITOR_RESP = 'Editor'
EDITOR = 'user@nyu.edu'
DATE_RESP = 'Date'
PUBLISHER = "pub"
PUBLISHER_RESP = 'Publisher'
RETURN = 'return'
DATE = '2024-09-24'
PEOPLE_EP = '/people'
TEXT_EP = '/text'
MANU_EP = '/manuscripts'
ROLES_EP = '/roles'
ERROR_LOG_EP = '/error_log'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading, updating,
    and deleting the journal title.
    """
    def get(self):
        """
        Retrieves the journal title.
        """
        return {TITLE_RESP: TITLE,
                EDITOR_RESP: EDITOR,
                DATE_RESP: DATE,
                PUBLISHER_RESP: PUBLISHER,
                }


'''
@api.route(PEOPLE_EP)
class People(Resource):
    def get(self):
        """
        Retrieves the journal people.
        """
        return ppl.read()
'''
PEOPLE_DELETE_FLDS = api.model('DeletePeopleEntry', {
    ppl.EMAIL: fields.String,
})
PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.PASSWORD: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.EMAIL: fields.String,
    ppl.ROLES: fields.List(fields.String)
})
PEOPLE_UPDATE_FLDS = api.model('UpdatePeopleEntry', {
    ppl.EMAIL: fields.String,
    ppl.NAME: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.List(fields.String)
})
PEOPLE_LOGIN_FLDS = api.model('TryLoginEntry', {
    ppl.EMAIL: fields.String,
    ppl.PASSWORD: fields.String,
})

# @api.route(f'{PEOPLE_EP}/<_id>')
@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self):
        """
        Retrieves the journal people.
        """
        return ppl.read()

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    @api.expect(PEOPLE_DELETE_FLDS)
    def delete(self):
        """
        Endpoint to delete a person
        """
        try:
            kwargs = {sec.LOGIN_KEY: "test key"}
            if not sec.is_permitted(sec.PEOPLE, sec.DELETE, sec.GOOD_USER_ID,
                                    **kwargs):
                raise wz.Forbidden("User doesn't have authorization")
            email = request.json.get(ppl.EMAIL)
            ret = ppl.delete(email)
        except Exception as err:
            logger.error(f'Error in DELETE people: {err}')
            raise wz.NotAcceptable(f'Could not delete person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Deleted!',
            RETURN: ret,
        }

    """
    Add a person to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            password = request.json.get(ppl.PASSWORD)
            roles = request.json.get(ppl.ROLES)
            ret = ppl.create(email, name, password, affiliation, roles)
        except Exception as err:
            logger.error(f'Error in PUT people: {err}')
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }
    """
    Update a person to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_UPDATE_FLDS)
    def patch(self):
        """
        Update a person.
        """
        try:
            _id = request.json.get(ppl.EMAIL)
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            roles = request.json.get(ppl.ROLES)
            ppl.update(_id, name, affiliation, roles)
        except Exception as err:
            logger.error(f'Error in UPDATE people: {err}')
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
            # commented cause getting error from the frontend if it returns ret
            # RETURN: ret,
        }
    """
    Try logging in
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_LOGIN_FLDS)
    def post(self):
        """
        Attempt a login
        """
        try:
            email = request.json.get(ppl.EMAIL)
            password = request.json.get(ppl.PASSWORD)
 
            ret = ppl.try_login(email, password)
        except Exception as err:
            logger.error(f'Error in POST people: {err}')
            raise wz.NotAcceptable(f'Login error: '
                                   f'{err=}')
        return {
            MESSAGE: 'Login Attempted!',
            RETURN: ret,
        }


PEOPLE_ROLE_UPD_FLDS = api.model('UpdatePeopleRoleEntry', {
    rls.CODE: fields.String,
})

EDITOR = 'editor'


@api.route(f'{PEOPLE_EP}/<email>/<user_id>')
class Person(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self, email, user_id):
        """
        Retrieve a journal person.
        """
        person = ppl.read_one(email)
        if person:
            return person
        else:
            logger.error(f'Error in GET person - No such record: {email}')
            raise wz.NotFound(f'No such record: {email}')

    @api.expect(PEOPLE_ROLE_UPD_FLDS)
    def patch(self, email, user_id):
        """
        Update role for person.
        """
        try:
            role = request.json.get(rls.CODE)
            print(role)
            ret = ppl.update_role(email, role)
        except Exception as err:
            logger.error(f'Error in UPDATE people/email/user_id: {err}')
            raise wz.NotAcceptable(f'Could not update person role: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person role updated!',
            RETURN: ret,
        }

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, email, user_id):
        kwargs = {sec.LOGIN_KEY: 'any key for now'}
        if not sec.is_permitted(sec.PEOPLE, sec.DELETE, user_id,
                                **kwargs):
            raise wz.Forbidden('This user does not have '
                               + 'authorization for this action.')
        ret = ppl.delete(email)
        if ret is not None:
            return {'Deleted': ret}
        else:
            logger.error(f'Error in DELETE person - No such person: {email}')
            raise wz.NotFound(f'No such person: {email}')

# @api.route(f'{PEOPLE_EP}/<_id>,<name>,<aff>')
# class PersonPut(Resource):
#     def put(self, _id, name, aff):
#         """
#         Endpoint to create a person
#         """
#         ret = ppl.create_person(_id, name, aff)
#         return {'Message': ret}


@api.route(f'{PEOPLE_EP}/<role>')
class CurrentPeople(Resource):
    """
    Retrieves people with a certain role.
    """
    def get(self, role):
        return ppl.get_ppl_in_role(role)


TEXT_CREATE_FLDS = api.model('AddNewTextEntry', {
    txt.KEY: fields.String,
    txt.TITLE: fields.String,
    txt.TEXT: fields.String
})
TEXT_UPDATE_FLDS = api.model('TextPeopleEntry', {
    txt.KEY: fields.String,
    txt.TITLE: fields.String,
    txt.TEXT: fields.String,
})
TEXT_DELETE_FLDS = api.model('DeleteTextEntry', {
    txt.KEY: fields.String,
})


@api.route(TEXT_EP)
class Text(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal text.
    """
    def get(self):
        """
        Retrieves journal text
        """
        return txt.read()

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_CREATE_FLDS)
    def put(self):
        """
        Add a text.
        """
        try:
            key = request.json.get(txt.KEY)
            title = request.json.get(txt.TITLE)
            text = request.json.get(txt.TEXT)
            ret = txt.create(key, title, text)
        except Exception as err:
            logger.error(f'Error in PUT text: {err}')
            raise wz.NotAcceptable(f'Could not add text: '
                                   f'{err=}')
        return {
            MESSAGE: 'Text added!',
            RETURN: ret,
        }

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_UPDATE_FLDS)
    def patch(self):
        """
        Update a text.
        """
        try:
            key = request.json.get(txt.KEY)
            title = request.json.get(txt.TITLE)
            text = request.json.get(txt.TEXT)
            ret = txt.update(key, title, text)
        except Exception as err:
            logger.error(f'Error in UPDATE text: {err}')
            raise wz.NotAcceptable(f'Could not update text: '
                                   f'{err=}')
        return {
            MESSAGE: 'Text updated!',
            RETURN: ret,
        }

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such text.')
    @api.expect(TEXT_DELETE_FLDS)
    def delete(self):
        """
        Endpoint to delete a text
        """
        try:
            key = request.json.get(txt.KEY)
            ret = txt.delete(key)
        except Exception as err:
            logger.error(f'Error in DELETE text: {err}')
            raise wz.NotAcceptable(f'Could not delete text: '
                                   f'{err=}')
        return {
            MESSAGE: 'Deleted!',
            RETURN: ret,
        }


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return ppl.get_masthead()


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manu.MANU_ID: fields.String,
    manu.CURR_STATE: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREE: fields.String,
    manu.NEW_STATE: fields.String,
    manu.REF_REPORT: fields.String,
    manu.REF_VERDICT: fields.String,
})

MANU_DELETE_FLDS = api.model('DeleteManu', {
    manu.MANU_ID: fields.String,
})

REFEREE_FLDS = api.model('Referee', {
    manu.REF_REPORT: fields.String,
    manu.REF_VERDICT: fields.String,
})
REFEREES_FLDS = api.model('Referees', {
    manu.REF_ID: fields.Nested(REFEREE_FLDS)
})

MANU_CREATE_FLDS = api.model('CreateManu', {
    manu.TITLE: fields.String,
    manu.AUTHOR: fields.String,
    manu.AUTHOR_EMAIL: fields.String,
    manu.TEXT: fields.String,
    manu.ABSTRACT: fields.String,
    manu.EDITOR_EMAIL: fields.String,
    manu.REFEREES: fields.Nested(REFEREES_FLDS)
})
MANU_UPDATE_FLDS = api.model('UpdateManu', {
    manu.TITLE: fields.String,
    manu.AUTHOR: fields.String,
    manu.AUTHOR_EMAIL: fields.String,
    manu.TEXT: fields.String,
    manu.ABSTRACT: fields.String,
    manu.EDITOR_EMAIL: fields.String,
})


# @api.route(f'{PEOPLE_EP}/<_id>')
@api.route(MANU_EP)
class Manuscript(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal manuscripts.
    """
    def get(self):
        """
        Retrieves the journal manuscripts.
        """
        return manu.read()

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such manuscript.')
    @api.expect(MANU_DELETE_FLDS)
    def delete(self):
        """
        Endpoint to delete a manuscript
        """
        try:
            # title = request.json.get(manu.TITLE)
            _id = request.json.get('_id')
            ret = manu.delete(_id)
        except Exception as err:
            logger.error(f'Error in DELETE manuscript: {err}')
            raise wz.NotAcceptable(f'Could not delete manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Deleted!',
            RETURN: str(ret),
        }

    """
    Add a manuscript to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_CREATE_FLDS)
    def put(self):
        """
        Add a manuscript.
        """
        try:
            title = request.json.get(manu.TITLE)
            author = request.json.get(manu.AUTHOR)
            author_email = request.json.get(manu.AUTHOR_EMAIL)
            text = request.json.get(manu.TEXT)
            abstract = request.json.get(manu.ABSTRACT)
            # editor_email = request.json.get(manu.EDITOR_EMAIL)
            referees = request.json.get(manu.REFEREES)
            ret = manu.create(title, author, author_email, text, abstract,
                              referees)
        except Exception as err:
            logger.error(f'Error in PUT manuscript: {err}')
            raise wz.NotAcceptable(f'Could not add manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript added!',
            RETURN: ret,
        }
    """
    Update a manuscript to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_UPDATE_FLDS)
    def patch(self):
        """
        Update a manuscript.
        """
        try:
            _id = request.json.get('_id')
            title = request.json.get(manu.TITLE)
            author = request.json.get(manu.AUTHOR)
            author_email = request.json.get(manu.AUTHOR_EMAIL)
            text = request.json.get(manu.TEXT)
            abstract = request.json.get(manu.ABSTRACT)
            editor_email = request.json.get(manu.EDITOR_EMAIL)
            manu.update(_id, title, author, author_email,
                        text, abstract, editor_email)
        except Exception as err:
            logger.error(f'Error in UPDATE manuscript: {err}')
            raise wz.NotAcceptable(f'Could not update manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript updated!',
            # RETURN: ret,
        }


@api.route(f'{MANU_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            print(request.json)
            _id = request.json.get(manu.MANU_ID)
            curr_state = request.json.get(manu.CURR_STATE)
            action = request.json.get(manu.ACTION)
            kwargs = {}
            kwargs[manu.REFEREE] = request.json.get(manu.REFEREE)
            kwargs[manu.NEW_STATE] = request.json.get(manu.NEW_STATE)
            kwargs[manu.REF_REPORT] = request.json.get(manu.REF_REPORT)
            kwargs[manu.REF_VERDICT] = request.json.get(manu.REF_VERDICT)
            ret = manu.handle_action(_id, curr_state, action, **kwargs)
        except Exception as err:
            logger.error(f'Error in receiving action: {err}')
            raise wz.NotAcceptable(f'Bad action: ' f'{err=}')
        return {
            MESSAGE: 'Action received!',
            RETURN: ret,
        }


@api.route(ROLES_EP)
class Roles(Resource):
    """
    This class handles creating, reading, updating
    and deleting roles.
    """
    def get(self):
        """
        Retrieves role types.
        """
        return rls.get_roles()


@api.route(f'{ROLES_EP}/masthead')
class MastheadRoles(Resource):
    """
    Get a journal's masthead roles.
    """
    def get(self):
        return rls.get_masthead_roles()


@api.route(f'{MANU_EP}/actions')
class Manu(Resource):
    """
    This class handles getting form components for manuscript.
    """
    def get(self):
        """
        Retrieves role types.
        """
        return manu.get_actions()


VALID_ACTION_INPUT = api.model('ValidActionInput', {
    'state': fields.String(required=True)
})


@api.route(f'{MANU_EP}/valid_actions')
class ValidActionsByState(Resource):
    @api.expect(VALID_ACTION_INPUT)
    def post(self):
        """
        Actions based on state
        """
        state = request.json.get('state')
        if not manu.is_valid_state(state):
            logger.error(f'Error in valid_actions- invalid state: {state}')
            raise wz.BadRequest(f"Invalid state: {state}")
        valid_actions = manu.get_valid_actions_by_state(state)
        return {"actions": valid_actions}


@api.route(f'{MANU_EP}/states')
class ManuStates(Resource):
    """
    This class handles getting form components for manuscript.
    """
    def get(self):
        """
        Retrieves states
        """
        return manu.get_states()


@api.route(ERROR_LOG_EP)
class ErrorLog(Resource):
    """
    Returns the contents of the error log,
    filtered to only show ERROR and CRITICAL entries,
    formatted as a list of dictionaries.
    """
    def get(self):
        log_path = 'logs/error.log'
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()

            error_entries = []
            for line in lines:
                if 'ERROR' in line or 'CRITICAL' in line:
                    match = re.match(
                        r'^(?P<timestamp>[\d\-:\s,]+)\s'
                        r'(?P<level>[A-Z]+):\s+'
                        r'(?P<message>.*)', line
                    )
                    if match:
                        error_entries.append(match.groupdict())
                    else:
                        error_entries.append({'raw': line.strip()})

            return {'errors': error_entries}, HTTPStatus.OK

        except FileNotFoundError:
            return {'message': 'Log file not found.'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error(f'Failed to read log file: {e}')
            raise wz.InternalServerError('Failed to read error log.')


@api.route(f'{MANU_EP}/verdicts')
class ManuVerdicts(Resource):
    def get(self):
        return manu.get_verdicts()
