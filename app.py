import os

from flask import Flask, redirect, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://localhost/vgs_sample'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    ssn = db.Column(db.String, unique=True, nullable=False)


@app.route('/')
def index():
    return render_template_string('''
    <a href="{{ url_for('.sign_up') }}">Sign up</a>
    ''')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template_string('''
        Sign-up to see your credit score:
        <form method="POST">
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


@app.route("/my-credit-score")
def my_credit_score():
    # TODO: handle my credit score here
    return "my_credit_score"