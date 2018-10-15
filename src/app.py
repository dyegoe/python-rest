from os import getenv
from flask import Flask, json, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from socket import gethostname
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'.format(
    db_user=getenv('DB_USER', 'db_user'),
    db_password=getenv('DB_PASSWORD', 'db_password'),
    db_host=getenv('DB_HOST', '172.17.0.2'),
    db_name=getenv('DB_NAME', 'db_name')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print('[INFO] SQLALCHEMY_DATABASE_URI = {0}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
print('[INFO] HOSTNAME = {0}'.format(gethostname()))

api = Api(app)


class DbNotes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(140), unique=False, nullable=False)
    creation = db.Column(db.DateTime, unique=False, nullable=False)
    update = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, note, creation, update):
        self.note = note
        self.creation = creation
        self.update = update
    #
    # def __repr__(self):
    #     return '%s(%s)' % (self.__class__.__name__, {
    #         column: value
    #         for column, value in self._to_dict().items()
    #     })
    #
    # def json(self):
    #     return {
    #         column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
    #         for column, value in self._to_dict().items()
    #     }


class ApiHome(Resource):
    def get(self):
        try:
            count_registers = DbNotes.query.filter_by().count()
            return {'status_code': '200', 'hostname': gethostname(),
                    'result': count_registers}, 200
        except Exception as e:
            return {'status_code': '501', 'hostname': gethostname(), 'error': str(e)}, 500


class ApiHealth(Resource):
    def get(self):
        try:
            count_registers = DbNotes.query.filter_by().count()
            return {'status_code': '200', 'hostname': gethostname(),
                    'result': count_registers}, 200
        except Exception as e:
            return {'status_code': '501', 'hostname': gethostname(), 'error': str(e)}, 500


class ApiList(Resource):
    def get(self):
        try:
            result = DbNotes.query.filter().all()
            return {'status_code': '200', 'hostname': gethostname(),
                    'result': 'none'}, 200
        except Exception as e:
            return {'status_code': '501', 'hostname': gethostname(), 'error': str(e)}, 500


class ApiCreate(Resource):
    def post(self):
        try:
            if request.headers['Content-Type'] == 'application/json':
                if 'note' in request.json:
                    insert = DbNotes(request.json['note'], datetime.datetime.now(), datetime.datetime.now())
                    db.session.add(insert)
                    db.session.commit()
                    return {'status_code': '200', 'hostname': gethostname(),
                            'Result': request.json['note']}, 200
                else:
                    raise Exception('Cannot find "notes" on the json')
            else:
                raise Exception('Content-Type {} not supported'.format(request.headers['Content-Type']))
        except Exception as e:
            return {'status_code': '501', 'hostname': gethostname(), 'error': str(e)}, 500


api.add_resource(ApiHome, '/notes/v1')
api.add_resource(ApiHealth, '/notes/v1/health')
api.add_resource(ApiList, '/notes/v1/list')
api.add_resource(ApiCreate, '/notes/v1/create')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
