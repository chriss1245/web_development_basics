from . import db
import flask_login

class FollowingAssociation(db.Model):
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True,
        nullable=False
    )

    followed_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True,
        nullable=False
    )

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True, nullable = False)
    name = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    messages = db.relationship('Message', backref = 'user', lazy = True)
    following = db.relationship(
        "User",
        secondary=FollowingAssociation.__table__,
        primaryjoin=FollowingAssociation.follower_id==id,
        secondaryjoin=FollowingAssociation.followed_id==id,
        backref='followers'
    )

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable = False)
    response_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    response_to = db.relationship('Message', backref = 'responses', remote_side=[id], lazy = True)
