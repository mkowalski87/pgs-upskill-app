from dblayer import User, Skill, UserSkill
from Exceptions import *
import boto3
import uuid

class UserService:

    def __init__(self, db):
        self.db = db

    def create_or_update(self, json):
        if 'id' in json:
            self.update_user(json)
        else:
            # create
            userObj = User(json)
            self.db.session.add(userObj)
            self.db.session.commit()

    def update_user(self, json):
        id = json['id']
        user = self.get_by_id(id)
        if user:
            user.first_name = json['first_name']
            user.last_name = json['last_name']
            self.db.session.merge(user)
            self.db.session.commit()

    def get_skills(self, user_id: int):
        user = self.get_by_id(user_id)
        if user is None:
            raise Exception("missing user")
        return user.skills

    def update_skills(self, id, skills):
        user = self.get_by_id(id)
        for skill in skills:
            skill_name = skill['name']
            skill_level = skill['level']
            user_skill = user.get_user_skill_by_name(skill_name)
            if user_skill is None:
                skill = self.get_skill_by_name_or_create(skill_name)
                user.skills.append(UserSkill(skill=skill, level = skill_level))
                pass
            else:
                user_skill.level = skill_level
        self.db.session.merge(user)
        self.db.session.commit()

    def delete_user(self, id):
        user = self.get_by_id(id)
        self.db.session.delete(user)
        self.db.session.commit()

    def all_users(self):
        return User.query.all()

    def get_by_id(self, id) -> User:
        user = User.query.filter(User.id == id).first()
        if user is None:
            raise NotFoundObjectError("User")
        return user

    def get_skill_by_name_or_create(self, name) -> Skill:
        skill = Skill.query.filter(Skill.name == name).first()
        if skill is None:
            skill = Skill(name=name)
            self.db.session.add(skill)
            self.db.session.commit()
        return skill

    def upload_cv(self, user_id, data):
        filename = "".join(['cv/', str(uuid.uuid4()), ".pdf"])
        s3 = boto3.resource('s3')
        s3.Bucket('mkowalski-upskill').put_object(Key=filename,Body=data)
        user = self.get_by_id(user_id)
        user.cv_url = filename
        self.db.session.merge(user)
        self.db.session.commit()


