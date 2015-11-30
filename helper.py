import json

from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import channel

from settings import EMAIL_SENDER
from models.card import *
from models.board import *
from models.user import *

class Entity:
    def get_board(self, board_id):
        return ndb.Key('Board', int(board_id)).get()

    def get_card(self, card_id):
        return ndb.Key('Card', int(card_id)).get()

    def current_ganban_user(self):
        print users.get_current_user()
        return User.query(User.google_id == users.get_current_user().user_id()).fetch(1)[0]

class Mailer:
    def send_new_card_email(self, card):
        emails = User.all_emails()

        message = mail.EmailMessage(sender = EMAIL_SENDER, subject = "New card created.")
        message.to = emails
        message.body = """
        A new card was created.

        Board: %s
        Author: %s
        Content: %s

        The Ganban Team
        """ % (card.board().name, self.current_ganban_user().username, card.content)

        message.send()

class Channel:
    def send_channel_message(self, action, card):
        for u in User.query(User.key != self.current_ganban_user().key).fetch():
            token = memcache.get(str(u.key.id()))
            if token:
                dic = {
                    'action' : action,
                    'card' : card.to_dict()
                }

                channel.send_message(token, json.dumps(dic))
