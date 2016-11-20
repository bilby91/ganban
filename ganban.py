import webapp2

from handlers import web
from handlers import api
from handlers import channel

from models.board import Board

# We need to initialize the default board on the application startup.
# We search for them, in case they are not present, we create them.
if not Board.query(Board.name == 'To Do').fetch(1):
    Board(name='To Do').put()

if not Board.query(Board.name == 'In Progress').fetch(1):
    Board(name='In Progress').put()

if not Board.query(Board.name == 'Done').fetch(1):
    Board(name='Done').put()

# Configure the WSGIApplication routes
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=web.RootHandler, methods=['GET']),
    webapp2.Route(r'/welcome', handler=web.WelcomeHandler, methods=['GET']),
    webapp2.Route(r'/api/cards', handler=api.CreateCardHandler, methods=['POST']),
    webapp2.Route(r'/api/cards/<card_id>', handler=api.GetCardHandler, methods=['GET']),
    webapp2.Route(r'/api/cards/<card_id>', handler=api.UpdateCardHandler, methods=['PUT']),
    webapp2.Route(r'/api/cards/<card_id>', handler=api.DestroyCardHandler, methods=['DELETE']),
    webapp2.Route(r'/_ah/channel/connected/', handler=channel.ConnectedHandler, methods=['POST']),
    webapp2.Route(r'/_ah/channel/disconnected/', handler=channel.DisconnectedHandler, methods=['POST'])
], debug=True)
