POSTGRES = {
    'user': 'postgres',
    'pw': 'daniel123',
    'db': 'examschedule',
    'host': 'localhost',
    'port': '5432',
}

config = {
    'SQLALCHEMY_DATABASE_URI': 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES,
    'SECRET_KEY': 'secret-key'
}