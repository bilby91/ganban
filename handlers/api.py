import webapp2, json, logging
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import channel

from settings import EMAIL_SENDER
from models.card import *
from models.board import *
from models.user import *

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if hasattr(obj, 'isoformat') else None)

class Helpers(object):
    def get_board(self, board_id):
        return ndb.Key('Board', int(board_id)).get()

    def get_card(self, card_id):
        return ndb.Key('Card', int(card_id)).get()

    def current_ganban_user(self):
        return User.query(User.google_id == users.get_current_user().user_id()).fetch(1)[0]

    def send_new_card_email(self, card):
        emails = User.all_emails()

        message = mail.EmailMessage(sender = EMAIL_SENDER, subject = "New card created.")
        message.to = emails
        message.body = """
        A new card was created in the Board %s

        Author: %s
        Content: %s

        The Ganban Team
        """ % (card.board().name, self.current_ganban_user().username, card.content)

        message.send()

    def send_channel_message(self, action, card):
        for u in User.query().fetch():
            token = memcache.get(str(u.key.id()))
            dic = {
                'action' : action,
                'card' : card.to_dict()
            }
            channel.send_message(token, json.dumps(dic))

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
            card.board_key = self.get_board(board_id).key

        card.put()

        self.send_channel_message('update', card)
        self.response.out.write(json.dumps(card.to_dict()))

class CreateCardHandler(ApiHandler):
    def post(self):
        board = self.get_board(self.request.get('board_id'))

        card = Card(board_key = board.key, content = self.request.get('content'), author_key = self.current_ganban_user().key)
        card.put()

        self.send_new_card_email(card)

        self.send_channel_message('create', card)
        self.response.out.write(json.dumps(card.to_dict()))

class DestroyCardHandler(ApiHandler):
    def delete(self, card_id):
        card = self.get_card(card_id)

        card.key.delete()

        self.send_channel_message('destroy', card)
        self.response.out.write(json.dumps({}))
