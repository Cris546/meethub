from google.appengine.ext import ndb

class CssiUser(ndb.Model):
    user_id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    username = ndb.StringProperty()

class Activity(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    user = ndb.StringProperty()

class Friend(ndb.Model):
    friend_id = ndb.StringProperty()
    your_id = ndb.StringProperty()
