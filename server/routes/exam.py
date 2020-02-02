from models import User, Exam, db
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
