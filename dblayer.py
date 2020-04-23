from flask_sqlalchemy import SQLAlchemy
from flask import escape

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    cv_url = db.Column(db.String, unique=True)

    def __init__(self, json):
        self.first_name = escape(json['first_name'])
        self.last_name = escape(json['last_name'])
        self.cv_url = None

    @staticmethod
    def validate(json):
        if json == None:
            return 'missing json object'
        if 'first_name' not in json:
            return 'missing first_name'
        if 'last_name' not in json:
            return 'missing last_name'
        return None

    @property
    def serialize(self):
       return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'cv_url': self.cv_url}
