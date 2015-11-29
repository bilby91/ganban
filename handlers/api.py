import webapp2, json, logging

from models.card import *
from models.board import *

from google.appengine.ext import ndb

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if hasattr(obj, 'isoformat') else None)

class Helpers(object):
    def get_board(self, board_id):
        return ndb.Key('Board', int(board_id)).get()

    def get_card(self, card_id):
        return ndb.Key('Card', int(card_id)).get()

class ApiHandler(Helpers, webapp2.RequestHandler):
    def dispatch(self):
        super(ApiHandler, self).dispatch()
        self.response.headers['Content-Type'] = 'application/json'

class GetCardHandler(ApiHandler):
    def get(self, card_id):
        card = self.get_card(card_id)

        self.response.out.write(json.dumps(card.to_dict()))

class UpdateCardHandler(ApiHandler):
    def put(self, card_id):
        card = self.get_card(card_id)
        content = self.request.get('content')
        board_id = self.request.get('board_id')

        if content:
            card.content = content

        if board_id:
            card.board = self.get_board(board_id).key

        card.put()

        self.response.out.write(json.dumps(card.to_dict()))

class CreateCardHandler(ApiHandler):
    def post(self):
        board = self.get_board(self.request.get('board_id'))

        card = Card(board = board.key, content = self.request.get('content'))
        card.put()

        self.response.out.write(json.dumps(card.to_dict()))

class DestroyCardHandler(ApiHandler):
    def delete(self, card_id):
        card = self.get_card(card_id)

        card.key.delete()

        self.response.out.write(json.dumps({}))
