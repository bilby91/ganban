# from google.appengine.ext import ndb
# # from models.card import *
# # from models.json import *
#
# BOARD_TO_DO_CODE = 'to-do'
# BOARD_DOING_CODE = 'doing'
# BOARD_DONE_CODE  = 'done'
#
# class Board(JSON, ndb.Model):
#     code = ndb.StringProperty();
#     name = ndb.StringProperty();
#     created_at = ndb.DateTimeProperty(auto_now_add = True)
#     updated_at = ndb.DateTimeProperty(auto_now = True)
#
#     def get_cards(self):
#         return Card.query(board = self.key).fetch()
#
# class Card(JSON, ndb.Model):
#     status = ndb.StringProperty();
#     content = ndb.StringProperty();
#     board = ndb.KeyProperty(kind = Board)
#     created_at = ndb.DateTimeProperty(auto_now_add = True)
#     updated_at = ndb.DateTimeProperty(auto_now = True)
#
# class JSON(object):
#     def to_dict(self):
#         dictionary = super(JSON ,self).to_dict()
#         if not self.key == None:
#             dictionary['id'] = self.key.id()
#         return dictionary
#
# class User(ndb.Model):
#     username = ndb.StringProperty();
#     email = ndb.StringProperty();
#     google_id = ndb.StringProperty();
