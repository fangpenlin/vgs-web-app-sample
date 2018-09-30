import os

from flask import Flask, render_template_string, request
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

    def __repr__(self):
        return '<User %r>' % self.id


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


@app.route("/my-credit-score")
def my_credit_score():
    # TODO: handle my credit score here
    return "my_credit_score"
