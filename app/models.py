from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(6))
    password = db.Column(db.String(200))

    def __repr__(self):
        return'<User id {},name{}>'.format(self.id,self.name)
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    poster = db.Column(db.String(100))
    postnote = db.Column(db.String(100000))
    pictures = db.Column(db.Text)
    category = db.Column(db.String(200))
    added = db.Column(db.DateTime,default=datetime.datetime.now())

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    comment = db.Column(db.String(100000))
    added = db.Column(db.DateTime,default=datetime.datetime.now())


