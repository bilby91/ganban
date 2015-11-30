import webapp2, logging

from google.appengine.api import channel
from google.appengine.api import memcache
from google.appengine.api import users
from models.user import *

class ConnectedHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.Key('User', int(self.request.get('from'))).get()

        logging.info('User %s has connected.', user.email)

class DisconnectedHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.Key('User', int(self.request.get('from'))).get()
        memcache.delete(str(user.key.id()))

        logging.info('User %s has disconnected.', user.email)
