from flask import Blueprint, jsonify, request
from models.db_engine import engine
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash


accounts_api = Blueprint('accounts_api', __name__)


@accounts_api.route('/all', methods=['GET'])
def get_all_accounts():
    conn = engine.connect()
    result = conn.execute('SELECT * FROM Admins')
    conn.close()
    return jsonify([dict(r) for r in result])


@accounts_api.route('/login', methods=['POST'])
def login():
    conn = engine.connect()
    error = None

    username = request.form['username']
    password = request.form['password']

    s = text('SELECT * from Admins WHERE Username = :username')
    user = conn.execute(s, username=username).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['Password'], password):
        error = 'Incorrect password.'

    if error is None:
        conn.close()
        return jsonify({'connected': True, 'user': {
            'username': user['Username'],
            'id': user['Id']
        }})

    conn.close()
    return jsonify({'connected': False, 'error': error})


@accounts_api.route('/new', methods=['POST'])
def add_account():
    # username, password, password_confirm required

    conn = engine.connect()

    username = request.form['username']
    password = request.form['password']
    password_confirm = request.form['password_confirm']

    error = _check_user_data(username, password, password_confirm)

    s = text('SELECT * FROM Admins WHERE Username = :x')
    existing_user = conn.execute(s, x=username).fetchone()
    if error is None and existing_user is not None:
        error = 'The username has already taken.'

    if error is None:
        s = text('INSERT INTO Admins(Username, Password) VALUES(:username, :password)')
        result = conn.execute(s, username=username, password=generate_password_hash(password))
        conn.close()
        return jsonify({'success': True, 'additional': dict(result)})

    conn.close()

    return jsonify({'success': False, 'error': error})


def _check_user_data(username, password, password_confirm=None):
    error = None

    if len(username) < 4:
        error = 'Username is too short.'

    if len(password) <= 8:
        error = 'Password is too short.'

    if password != password_confirm:
        error = 'Passwords doesn\'t matches.'

    return error
