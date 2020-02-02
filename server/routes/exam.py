from models import User, Subject, Exam, Application, Exam_period, db
from flask import request, Blueprint
from utils import custom_response
from flask_jwt import jwt_required, current_identity

exam_api = Blueprint('exam_api', __name__)


@exam_api.route('/exam', methods=['POST'])
@jwt_required()
def add_exam():
    if current_identity.is_superuser:
        data = request.get_json()
        exam = Exam(data['subject_id'], data['exam_period_id'], data['date'])
        exam.save()
        return custom_response({'message': 'Successfully created'}, 201)
    else:
        return custom_response({'error': 'Unauthorized'}, 403)


@exam_api.route('/exam/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_exam(id):
    if current_identity.is_superuser:
        Exam.query.filter_by(id=id).delete()
        db.session.commit()
        return custom_response({'message': 'Successfully deleted'}, 204)
    else:
        return custom_response({'error': 'Unauthorized'}, 403)

@exam_api.route('/exam/<int:id>', methods=['PATCH'])
@jwt_required()
def update_exam(id):
    if current_identity.is_superuser:
        exam = Exam.query.filter_by(id=id)
        data = request.get_json()
        if 'date' in data:
            switch = {
                'date': data['date']
            }
        else:
            return custom_response({'error':'Bad request'},400)

        exam.update(values=switch)
        db.session.commit()

        updated_exam = Exam.query.get(id)
        # updated_exam = Exam(updated_exam['id'], )

        return custom_response(updated_exam.serialize(), 202)
    else:
        return custom_response({'error': 'Unauthorized'}, 403)


@exam_api.route('/subjects')
def getSubjects():
    # year query parametar
    year = request.args.get('year')
    if year:
        subjects = Subject.query.filter(Subject.year == year)
    else:
        subjects = Subject.query.all()
    subjects_json = [subject.serialize() for subject in subjects]
    return custom_response(subjects_json)


@exam_api.route('/apply', methods=['POST'])
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

@exam_api.route('/applied', methods=['GET'])
@jwt_required()
def getAppliedExams():
    userID = current_identity.id
    applied_exams = Application.query.filter(Application.user_id == userID)
    print(applied_exams)
    for exam in applied_exams:
        print(exam.serialize())
 
    exams_json = [application.serialize() for application in applied_exams]
    return custom_response(exams_json)

@exam_api.route('/cancel-application/<int:application_id>', methods=['POST'])
@jwt_required()
def cancelApplication(application_id):
    application = Application.query.get(application_id)
    if application and application.user_id == current_identity.id:
        print("Canceling application")
        print(application.serialize())
        db.session.delete(application)
        db.session.commit()
        return custom_response({'message':'Application cancelation successful.'})
    else:
        return custom_response({'message':'User application not found.'}, 403)


@exam_api.route('/exam-periods', methods=['GET'])
def getExamPeriod():
    exam_periods = Exam_period.query.all()
    exam_periods_json = [period.serialize() for period in exam_periods]
    return custom_response(exam_periods_json)