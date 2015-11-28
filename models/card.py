from google.appengine.ext import ndb

class Card(ndb.Model):
    id = ndb.ComputedProperty(lambda self: self.key.id())
    status = ndb.StringProperty();
    content = ndb.StringProperty();
    created_at = ndb.DateTimeProperty(auto_now_add = True)
    updated_at = ndb.DateTimeProperty(auto_now = True)
