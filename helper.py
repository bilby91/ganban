from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import channel

from settings import EMAIL_SENDER
from models.card import *
from models.board import *
from models.user import *

class Entities:

    def get_board(self, board_id):
        return ndb.Key('Board', int(board_id)).get()

    def get_card(self, card_id):
        return ndb.Key('Card', int(card_id)).get()

    def current_ganban_user(self):
        print users.get_current_user()
        return User.query(User.google_id == users.get_current_user().user_id()).fetch(1)[0]
