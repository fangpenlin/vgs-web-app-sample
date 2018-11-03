import os

import requests
from flask import Flask, redirect, render_template_string, request, url_for
from flask.cli import AppGroup, with_appcontext
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://localhost/vgs_sample'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
utils_cli = AppGroup('utils')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    ssn = db.Column(db.String, unique=True, nullable=False)


@utils_cli.command('create_tables')
@with_appcontext
def create_tables():
    db.create_all()

app.cli.add_command(utils_cli)

@app.route('/')
def index():
    return render_template_string('''
    <ul>
        <li><a href="{{ url_for('.sign_up') }}">Sign up</a></li>
        <li><a href="{{ url_for('.my_credit_score') }}">Check my credit score</a></li>
    </ul>
    ''')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template_string('''
        Sign-up to:
        <form method="POST" action="https://tntsyv550xu.SANDBOX.verygoodproxy.com/sign-up">
            <div>
                <label for="email">Email:</label>
                <input name="email" />
            </div>
            <div>
                <label for="ssn">Social Security Number:</label>
                <input name="ssn" />
            </div>
            <div>
                <input type="submit" />
            </div>
        </form>
        ''')
    email = request.form['email']
    ssn = request.form['ssn']
    user = User(
        email=email,
        ssn=ssn,
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('my_credit_score'))


@app.route('/my-credit-score', methods=['GET', 'POST'])
def my_credit_score():
    if request.method == 'GET':
        return render_template_string('''
        Enter your email to see your credit score:
        <form method="POST">
            <div>
                <label for="email">Email:</label>
                <input name="email" />
            </div>
            <div>
                <input type="submit" />
            </div>
        </form>
        ''')
    email = request.form['email']
    user = User.query.filter_by(email=email).first_or_404()
    api_url = os.environ['CREDIT_SCORE_API_URL']
    resp = requests.get(api_url + '?ssn=' + user.ssn)
    return render_template_string('''
    Your credit score is: {{score}}    
    ''', score=resp.json()['credit_score'])
