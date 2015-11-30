import webapp2, random, logging

from settings import JINJA_ENVIRONMENT
from google.appengine.api import channel
from google.appengine.api import memcache
from google.appengine.api import users
from models.user import *
from models.board import *


class RootHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            # Filter by the google appengine user id property.
            active_user = User.query(User.google_id == user.user_id()).fetch(1)

            if not active_user:
                # If we couldn't find a user it means that is the first time it uses the application.
                # We just need to create a new entity with the get_current_user() information.
                active_user = User(email = user.email(), username = user.nickname(), google_id = user.user_id())
                active_user.put()
                logging.info("New user created. Email address is: %s", new_user.email)
            else:
                active_user = active_user[0]

            token = channel.create_channel(str(active_user.key.id()))
            memcache.add(key=str(active_user.key.id()), value=token)
            template_vars = {
                'user' : active_user,
                'token' : token,
                'logout_url' : users.create_logout_url('/welcome'),
                'boards' : Board.query().order(Board.created_at)

            }
            template = JINJA_ENVIRONMENT.get_template('root.html')
            self.response.write(template.render(template_vars))
        else:
            self.redirect('/welcome')


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if not user:
            template = JINJA_ENVIRONMENT.get_template('welcome.html')
            self.response.write(template.render(login_url=users.create_login_url('/')))
        else:
            self.redirect('/')
