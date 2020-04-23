from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    cv_url = db.Column(db.String, unique=True)

    @property
    def serialize(self):
       return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'cv_url': self.cv_url}
