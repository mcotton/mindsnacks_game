from google.appengine.ext import db

class Board(db.Model):
    id = db.IntegerProperty()
    positions = db.StringProperty()


class LeaderBoard(db.Model):
   username = db.StringProperty()
   score = db.IntegerProperty()
   game_id = db.IntegerProperty()


