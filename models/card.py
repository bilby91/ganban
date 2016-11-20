from google.appengine.ext import ndb
from models.user import User
from models.json import JSON


class Card(JSON, ndb.Model):
    content = ndb.StringProperty()
    board_key = ndb.KeyProperty(kind='Board')
    author_key = ndb.KeyProperty(kind=User)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    def board(self):
        return self.board_key.get()

    def author(self):
        return self.author_key.get()

    def to_dict(self):
        dictionary = super(Card ,self).to_dict()
        dictionary.pop('board_key', None)
        dictionary.pop('author_key', None)

        if not self.board_key == None:
            dictionary['board_id'] = self.board_key.id()

        if not self.author_key == None:
            dictionary['author_email'] = self.author().email

        return dictionary
