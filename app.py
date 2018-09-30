import os

from flask import Flask
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


@app.route("/")
def register():
    # TODO: handle sign up here
    return "register"


@app.route("/")
def login():
    # TODO: handle sign in here
    return "login"


@app.route("/")
def my_credit_score():
    # TODO: handle my credit score here
    return "my_credit_score"
