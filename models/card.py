from google.appengine.ext import ndb
from models.board import *
from models.json import *

class Card(JSON, ndb.Model):
    content = ndb.StringProperty();
    board_key = ndb.KeyProperty(kind = Board)
    created_at = ndb.DateTimeProperty(auto_now_add = True)
    updated_at = ndb.DateTimeProperty(auto_now = True)

    def board(self):
        return self.board_key.get()

    def to_dict(self):
        dictionary = super(Card ,self).to_dict()
        dictionary.pop('board', None)

        if not self.board == None:
            dictionary['board_id'] = self.board_key.id()

        return dictionary
