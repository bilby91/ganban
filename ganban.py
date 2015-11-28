import webapp2

from handlers import web
from handlers import api

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler = web.RootHandler, methods = ['GET']),
    webapp2.Route(r'/welcome', handler = web.WelcomeHandler, methods = ['GET']),
    webapp2.Route(r'/cards', handler = api.GetCardListHandler, methods = ['GET']),
    webapp2.Route(r'/cards', handler = api.CreateCardHandler, methods = ['POST']),
    webapp2.Route(r'/cards/<card_id>', handler = api.GetCardHandler, methods = ['GET']),
    webapp2.Route(r'/cards/<card_id>', handler = api.UpdateCardHandler, methods = ['PUT']),
    webapp2.Route(r'/cards/<card_id>', handler = api.DestroyCardHandler, methods = ['DELETE'])
], debug=True)
