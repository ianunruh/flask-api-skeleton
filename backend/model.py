from datetime import datetime

from sqlalchemy_utils import PasswordType, force_auto_coercion

from backend.app import db
from backend.util import generate_token

# http://sqlalchemy-utils.readthedocs.io/en/latest/listeners.html#automatic-data-coercion
force_auto_coercion()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    password = db.Column(PasswordType(
        schemes=[
            'sha256_crypt',
        ]
    ))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_changed_at = db.Column(db.DateTime)

    sessions = db.relationship('Session', backref='user', lazy='dynamic')

    @classmethod
    def find_by_email_or_username(cls, username):
        return (User.query
                    .filter((User.email==username) | (User.username==username))
                    .first())

    def change_password(self, password):
        self.password = password
        self.password_changed_at = datetime.utcnow()


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    token = db.Column(db.String(255), default=generate_token)

    user_agent = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    platform = db.Column(db.String(255))
    browser = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active_at = db.Column(db.DateTime, default=datetime.utcnow)
