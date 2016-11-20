import os, jinja2

EMAIL_SENDER = "Ganban <team@ganban-1130.appspotmail.com>"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)
