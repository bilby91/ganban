import webapp2, urllib, random

from settings import JINJA_ENVIRONMENT
from google.appengine.api import users

class RootHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template_vars = {
                'user' : user,
                'logout_url' : users.create_logout_url('/welcome'),
                'containers' : [
                    {
                        'id' : 'to-do',
                        'name' : 'To do'
                    },
                    {
                        'id' : 'in-progress',
                        'name' : 'In Progress'
                    },
                    {
                        'id' : 'done',
                        'name' : 'Done'
                    }
                ],
                'cards' : [
                    [
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        },
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        },
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        }
                    ],
                    [
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        },
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        },
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        }
                    ],
                    [
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        },
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        },
                        {
                            'id' : random.randrange(1000, 10000, 1),
                            'content' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere purus. Phasellus in molestie libero. Vivamus mollis massa orci.'
                        }
                    ]
                ]
            }
            template = JINJA_ENVIRONMENT.get_template('templates/root.html')
            self.response.write(template.render(template_vars))
        else:
            self.redirect('/welcome')


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if not user:
            template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
            self.response.write(template.render(login_url=users.create_login_url('/')))
        else:
            self.redirect('/')
