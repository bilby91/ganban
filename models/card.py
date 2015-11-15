from google.appengine.ext import ndb

class Card(ndb.Model):
    content = ndb.StringProperty();
