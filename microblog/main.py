import datetime
import dateutil.tz
from . import model, default

from flask import Blueprint, render_template
import flask_login

bp = Blueprint("main", __name__)


@bp.route("/")
@flask_login.login_required
def index():
    user = model.User(email= "mary@example.com", name= "mary")
    posts = [
        model.Message(
            user = user,
            text = "Test post", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user,
            text = "Why i think we live in a parties dictatorship: \
                We do not select governors, we select parties who decide \
                who the govenors are.", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user,
            text = "What do you guys think", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        )
    ]
    return render_template("main/index.html", posts=posts)


@bp.route("/profile")
@flask_login.login_required
def profile():
    user = flask_login.current_user
    user.photo =  default.PHOTO
    posts = model.Message.query.filter_by(user=user)
    """
    posts = [
        model.Message(
            user = user,
            text = "Test post", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user,
            text = "Why i think we live in a parties dictatorship: \
                We do not select governors, we select parties who decide \
                who the govenors are.", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user,
            text = "What do you guys think", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        )
    ]  """
    return render_template("main/profile.html", user=user, posts=posts)

@bp.route("/messages")
@flask_login.login_required
def messages():
    user = model.User(email= "mary@example.com", name= "mary")
    users = [model.User(email= name+ "@example.com", name= name)\
         for name in ['emilio', 'pablo', 'rosa', 'hilda']]


    message = model.Message(
            user = user,
            text = "Why i think we live in a parties dictatorship: \
                We do not select governors, we select parties who decide \
                who the govenors are.", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        )

    replies = [model.Message(
            user = users[i+2],
            text = text, 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ) for i, text in zip(range(4), ['coll', 'great', 'rt', 'love you'])]
    return render_template("main/message.html",
        post = message,
        user = user,
        n_replies = len(replies), 
        replies =replies)