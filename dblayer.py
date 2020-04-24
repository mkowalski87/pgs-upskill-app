from flask_sqlalchemy import SQLAlchemy
from flask import escape

db = SQLAlchemy()

class UserSkill(db.Model):
    __tablename__ = 'user_skill_associations'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    skill_id = db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    user = db.relationship("User")
    skill = db.relationship("Skill")

    @property
    def serialized(self):
        return {'name': self.skill.name, 'level': self.level}


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    cv_url = db.Column(db.String, unique=True)
    skills = db.relationship('UserSkill')

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
    def serialized(self):
       return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'cv_url': self.cv_url, 'skills': [s.serialized for s in self.skills]}


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    @property
    def serialized(self):
       return {'id': self.id, 'name': self.name}

