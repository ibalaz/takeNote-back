import cx_Oracle
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(16)

try:
    """
    Connecting to database
    """
    dsn_tns = cx_Oracle.makedsn('bakidb.cop7bayjukim.eu-central-1.rds.amazonaws.com', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user=r'admin', password='Baki0902', dsn=dsn_tns, encoding='UTF-8')

    if conn.ping() is None:
        print('Connected to database server version', conn.version)
        cursor = conn.cursor()

except Exception as e:
    print('Error while connecting to database', e)


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    passw = request.form['password']
    email = request.form['email']
    userCount = cursor.var(int)

    if username:
        print('Login with username {}'.format(username))
        cursor.callproc('login_user', [username, passw, '', userCount])
    elif email:
        print('Login with email {}'.format(email))
        cursor.callproc('login_user', ['', passw, email, userCount])

    if userCount.getvalue() == 1:
        print('User {} exists. Login success!'.format(username))
        session['username'] = username
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'No such user in database, please register first!'})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'success': True})


@app.route('/register_user', methods=['POST'])
def register_user():
    if request.form['name'] and request.form['lastname'] and request.form['usercity'] and request.form['isprivate'] and \
            request.form['user'] and request.form['pass'] and request.form['mail'] in request.args:
        cursor.callproc('ADD_USER', [])
        return jsonify({'success': True})
    else:
        return jsonify({'success': False,
                        'error': 'Missing some of input parameters, input parameters are: name, lastname, usercity, isprivate, user, pass, mail'})


if __name__ == '__main__':
    app.run()
