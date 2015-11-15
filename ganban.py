import os, sys, urllib
import webapp2
import jinja2
from google.appengine.api import users
from models.user import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class RootHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template = JINJA_ENVIRONMENT.get_template('templates/home.html')
            self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
    ('/', RootHandler),
], debug=True)
