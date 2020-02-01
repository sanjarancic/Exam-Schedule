from models import User, Subject, Exam, Application, db
from flask import request, Blueprint
from utils import custom_response
from flask_jwt import jwt_required, current_identity
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
@jwt_required()
def applyForExam():
    examID = request.json['examID']
    exam = Exam.query.filter(Exam.id == examID).first()
    if exam:
        print('User {} is trying to apply for exam id {}'.format(current_identity.username, exam.id))
        application = Application(user_id=current_identity.id, exam_id=exam.id)
        application.save()
        return custom_response({'message':'Application successful.'})
    else:
        return custom_response({'message':'Application failed.'}, 400)

@exams_api.route('/applied', methods=['GET'])
@jwt_required()
def getAppliedExams():
    userID = current_identity.id
    applied_exams = Application.query.filter(Application.user_id == userID)
    print(applied_exams)
    for exam in applied_exams:
        print(exam.serialize())

    exams_json = [application.serialize() for application in applied_exams]
    return custom_response(exams_json)