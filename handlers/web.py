import webapp2
from settings import JINJA_ENVIRONMENT
from google.appengine.api import users

class RootHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template = JINJA_ENVIRONMENT.get_template('home.html')
            self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))
