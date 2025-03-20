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
            email = request.json.get(ppl.EMAIL)
            ret = ppl.delete(email)
        except Exception as err:
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
            roles = request.json.get(ppl.ROLES)
            ret = ppl.create(email, name, affiliation, roles)
        except Exception as err:
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
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
            # commented cause getting error from the frontend if it returns ret
            # RETURN: ret,
        }


PEOPLE_ROLE_UPD_FLDS = api.model('UpdatePeopleRoleEntry', {
    rls.CODE: fields.String,
})


@api.route(f'{PEOPLE_EP}/<email>')
class Person(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self, email):
        """
        Retrieve a journal person.
        """
        person = ppl.read_one(email)
        if person:
            return person
        else:
            raise wz.NotFound(f'No such record: {email}')

    @api.expect(PEOPLE_ROLE_UPD_FLDS)
    def patch(self, email):
        """
        Update role for person.
        """
        try:
            role = request.json.get(rls.CODE)
            print(role)
            ret = ppl.update_role(email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person role: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person role updated!',
            RETURN: ret,
        }

# @api.route(f'{PEOPLE_EP}/<_id>,<name>,<aff>')
# class PersonPut(Resource):
#     def put(self, _id, name, aff):
#         """
#         Endpoint to create a person
#         """
#         ret = ppl.create_person(_id, name, aff)
#         return {'Message': ret}


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
        return {MASTHEAD: ppl.get_masthead()}


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manu.TITLE: fields.String,
    manu.CURR_STATE: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREE: fields.String,
})

MANU_DELETE_FLDS = api.model('DeleteManu', {
    manu.TITLE: fields.String,
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
    ppl.EMAIL: fields.String,
    ppl.NAME: fields.String,
    ppl.AFFILIATION: fields.String,
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
            title = request.json.get(manu.TITLE)
            ret = manu.delete(title)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not delete manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Deleted!',
            RETURN: ret,
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
            editor_email = request.json.get(manu.EDITOR_EMAIL)
            referees = request.json.get(manu.REFEREES)
            ret = manu.create(title, author, author_email, text, abstract,
                              editor_email, referees)
        except Exception as err:
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
            title = request.json.get(manu.TITLE)
            author = request.json.get(manu.AUTHOR)
            author_email = request.json.get(manu.AUTHOR_EMAIL)
            text = request.json.get(manu.TEXT)
            abstract = request.json.get(manu.ABSTRACT)
            editor_email = request.json.get(manu.EDITOR_EMAIL)
            referees = request.json.get(manu.REFEREES)
            manu.update(title, author, author_email,
                        text, abstract, editor_email, referees)
        except Exception as err:
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
            title = request.json.get(manu.TITLE)
            curr_state = request.json.get(manu.CURR_STATE)
            action = request.json.get(manu.ACTION)
            kwargs = {}
            kwargs[manu.REFEREE] = request.json.get(manu.REFEREE)
            ret = manu.handle_action(title, curr_state, action, **kwargs)
        except Exception as err:
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
