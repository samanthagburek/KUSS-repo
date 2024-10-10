"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask  # request
from flask_restx import Resource, Api, fields  # Namespace
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.people as ppl

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


@api.route(f'{PEOPLE_EP}/<_id>')
class PersonDelete(Resource):
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, _id):
        """
        Endpoint to delete a person
        """
        ret = ppl.delete(_id)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.Not_Found(f'No such person: {_id}')


@api.route(f'{PEOPLE_EP}/<_id>,<name>,<aff>')
class PersonPut(Resource):
    def put(self, _id, name, aff):
        """
        Endpoint to create a person
        """
        ret = ppl.create_person(_id, name, aff)
        return {'Message': ret}


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
})
