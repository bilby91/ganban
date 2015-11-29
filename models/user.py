from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty();
    email = ndb.StringProperty();
    google_id = ndb.StringProperty();

    @staticmethod
    def all_emails():
        return User.query().map(lambda user: user.email)
