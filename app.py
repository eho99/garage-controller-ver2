import json
from functools import wraps

from flask import Flask, request, session, redirect, url_for, render_template
import flask_login

app = Flask(__name__)
app.secret_key = 'd7c88cb6c065663495f3cc47530b13119bde5a4898e51d75'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

GARAGE_STATUS = "Closed"

with open('logins.json') as f:
    users = json.load(f)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return None

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_load(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]
    return user


@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    input_username = request.form['username']
    input_password = request.form['password']
    if not (input_username == "" and input_password == ""):
        if input_password == users[input_username]:
            user = User()
            user.id = input_username
            flask_login.login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html', error="Invalid Login")


@app.route('/index', methods=["GET", "POST"])
@flask_login.login_required
def index():
    if request.method == 'GET':
        return render_template('index.html', status=GARAGE_STATUS)
    # else:
    #     if request.form


# Test for login information
@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


### former login
# try:
#     error = ''
#     if request.method == "POST":
#         attempted_username = request.form['username']
#         attempted_password = request.form['password']
#         if attempted_username == 'admin' and attempted_password == os.environ['USER_PASSWORD']:
#             session['logged_in'] = True
#             session['username'] = request.form['username']
#             return "big man"
#         else:
#             print('invalid credentials')
#             error = 'Invalid credentials. Please, try again.'
#     return render_template('login.html', error=error)
# except Exception as e:
#     return render_template('login.html', error=str(e))


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        """login session"""
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            pass
        return redirect(url_for('login'))

    return wrap


if __name__ == '__main__':
    app.run()
