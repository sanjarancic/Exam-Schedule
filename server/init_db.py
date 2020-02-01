from models import Subject, User
import json


def initialize_subjects():
    subjects_in_db = Subject.query.all()

    if not subjects_in_db:
        with open('subjects.json', 'r') as file:
            subjects = json.loads(file.read())

        for (year, subjects_in_year) in enumerate(subjects, start=1):
            for subject_name in subjects_in_year:
                s = Subject(subject_name, year)
                s.save()


def initialize_superuser():
    superuser = User.get_by_username('superuser')

    if not superuser:
        superuser = User('superuser', 'superuser', True)
        superuser.save()


