from google.appengine.ext import ndb
from models.json import *
from models.card import *

class Board(JSON, ndb.Model):
    name = ndb.StringProperty();
    created_at = ndb.DateTimeProperty(auto_now_add = True)
    updated_at = ndb.DateTimeProperty(auto_now = True)

    def cards(self):
        return Card.query(Card.board_key == self.key).fetch()
