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
})
PEOPLE_UPDATE_FLDS = api.model('UpdatePeopleEntry', {
    ppl.EMAIL: fields.String,
    ppl.NAME: fields.String,
    ppl.AFFILIATION: fields.String,
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
            role = request.json.get(ppl.ROLES)
            ret = ppl.create(email, name, affiliation, role)
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
        pass
        try:
            _id = request.json.get(ppl.EMAIL)
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            ret = ppl.update(_id, name, affiliation)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
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
        pass
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
