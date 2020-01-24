from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import math


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(70), index = True)
   username = db.Column(db.String(30), index = True, unique = True)
   email = db.Column(db.String(120), index = True, unique = True)
   password_hash = db.Column(db.String(128))
   posts = db.relationship('Post', backref='author', lazy='dynamic')
   comments = db.relationship('Comment', backref='author', lazy='dynamic')

   def __repr__(self):
      return "<User - {}>".format(self.username)

   def set_password(self, password):
      self.password_hash = generate_password_hash(password)

   def check_password(self, password):
      return check_password_hash(self.password_hash, password)

   def avatar(self, size):
      digest = md5(self.email.lower().encode('utf-8')).hexdigest()
      return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)

class Post(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   title = db.Column(db.String(140))
   body = db.Column(db.String(7000))
   timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
   comments = db.relationship('Comment', backref='article', lazy='dynamic')
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

   def __repr__(self):
      return "<Post - {}>".format(self.title)

   def shorten_txt(self):
      hold = ""
      if len(self.body) > 5000:
         for i in range(math.floor(len(self.body)/24)):
            hold += self.body[i]
         hold += "..."
         result = hold
         hold = ""
         return result
      elif len(self.body) in range(2500, 4999):
         for i in range(math.floor(len(self.body)/22)):
            hold += self.body[i]
         hold += "..."
         result = hold
         hold = ""
         return result
      elif len(self.body) in range(1500, 2499):
         for i in range(math.floor(len(self.body)/22)):
            hold += self.body[i]
         hold += "..."
         result = hold
         hold = ""
         return result
      else:
         for i in range(math.floor(len(self.body)/7.2)):
            hold += self.body[i]
         hold += "..."
         result = hold
         hold = ""
         return result

class Comment(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   saying = db.Column(db.String(250))
   comment_tmestp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

   def __repr__(self):
      return "<Comment - {}>".format(self.saying)

@login.user_loader
def load_user(id):
   return User.query.get(int(id))