from models import User, Subject
from flask import request, Blueprint
from utils import custom_response
from flask_jwt import jwt_required
from flask import jsonify

exams_api = Blueprint('exams_api', __name__)


@exams_api.route('/subjects')
def getSubjects():
    # year query parametar
    year = request.args.get('year')
    if year:
        subjects = Subject.query.filter(Subject.year == year)
    else:
        subjects = Subject.query.all()
    subjects_json = [subject.serialize() for subject in subjects]
    return custom_response(subjects_json)


@exams_api.route('/apply', methods=['POST'])
def applyForExam():
    print('Applying for exam')
