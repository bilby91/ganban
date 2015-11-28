import webapp2, json, logging

from models.card import *
from google.appengine.ext import ndb

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if hasattr(obj, 'isoformat') else None)

class ApiHandler(webapp2.RequestHandler):
    def dispatch(self):
        super(ApiHandler, self).dispatch()
        self.response.headers['Content-Type'] = 'application/json'

class GetCardHandler(ApiHandler):
    def get(self, card_id):
        card = ndb.Key('Card', int(card_id)).get().to_dict()

        self.response.out.write(json.dumps(card))

class GetCardListHandler(webapp2.RequestHandler):
    def get(self):
        cards = [card.to_dict() for card in Card.query()]

        self.response.out.write(json.dumps(cards))

class UpdateCardHandler(webapp2.RequestHandler):
    def put(self):
        return ''

class CreateCardHandler(webapp2.RequestHandler):
    def post(self):
        card = Card(status=self.request.get('status'), content=self.request.get('status'))
        card.put()

        self.response.out.write(json.dumps(card.to_dict()))

class DestroyCardHandler(webapp2.RequestHandler):
    def destroy(self, card_id):
        ndb.Key('Card', int(card_id)).delete()

        self.response.out.write(json.dumps({}))
