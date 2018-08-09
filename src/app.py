from os import getenv
from flask import Flask
from flask_restful import Resource, Api
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = getenv('MYSQL_DATABASE_USER', 'root')
app.config['MYSQL_DATABASE_PASSWORD'] = getenv('MYSQL_DATABASE_PASSWORD', 'password')
app.config['MYSQL_DATABASE_DB'] = getenv('MYSQL_DATABASE_DB', 'db')
app.config['MYSQL_DATABASE_HOST'] = getenv('MYSQL_DATABASE_HOST', 'localhost')


mysql.init_app(app)

api = Api(app)


class Health(Resource):
    def get(self):
        return {'StatusCode': '200', 'Status': 'Healthy', 'Hostname': getenv('HOSTNAME')}


class Users(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()

            users = [];
            for item in data:
                i = {
                    'Name': item[0],
                    'Age': item[1]
                }
                users.append(i)

            return {'StatusCode': '200', 'Hostname': getenv('HOSTNAME'), 'Users': users}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(Health, '/')

api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)