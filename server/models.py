import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String,unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String,unique=True)
    password = db.Column(db.String)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, password):
        self.username = username
        self.password = self.__generate_hash(password)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @staticmethod
    def get_by_username(value):
        return User.query.filter_by(username=value).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Exam_period(db.Model):
    __tablename__ = 'exam_periods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)

    def __init__(self, name, date_from, date_to):
        self.name = name
        self.date_from = date_from
        self.date_to = date_to

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_from': self.date_from,
            'date_to': self.date_to
        }

class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, ForeignKey('subjects.id'))
    exam_period_id = db.Column(db.Integer, ForeignKey('exam_periods.id'))
    date = db.Column(db.DateTime)

    def __init__(self, subject_id, exam_period_id, date):
        self.subject_id = subject_id
        self.exam_period_id = exam_period_id
        self.date = date

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'exam_period_id': self.exam_period_id,
            'date': self.date
        }

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, ForeignKey('exams.id'))

    def __init__(self, user_id, exam_id):
        self.user_id = user_id
        self.exam_id = exam_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'exam_id': self.exam_id
        }