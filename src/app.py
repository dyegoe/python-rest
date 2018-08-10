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

print("[INFO] MYSQL_DATABASE_USER = {0}".format(app.config['MYSQL_DATABASE_USER']))
print("[INFO] MYSQL_DATABASE_PASSWORD = {0}".format(app.config['MYSQL_DATABASE_PASSWORD']))
print("[INFO] MYSQL_DATABASE_DB = {0}".format(app.config['MYSQL_DATABASE_DB']))
print("[INFO] MYSQL_DATABASE_HOST = {0}".format(app.config['MYSQL_DATABASE_HOST']))
print("[INFO] HOSTNAME = {0}".format(getenv('HOSTNAME')))

mysql.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        return {'Hostname': getenv('HOSTNAME')}, 200


class Health(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            conn.close()
            return {'StatusCode': '200', 'Status': 'Healthy', 'Hostname': getenv('HOSTNAME')}, 200

        except Exception as e:
            return {'StatusCode': '500', 'error': str(e)}, 500


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
            conn.close()
            return {'StatusCode': '200', 'Hostname': getenv('HOSTNAME'), 'Users': users}, 200

        except Exception as e:
            return {'StatusCode': '500', 'error': str(e)}, 500


api.add_resource(Home, '/')
api.add_resource(Health, '/health')
api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)