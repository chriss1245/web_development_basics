import datetime
import dateutil.tz
from . import default

from flask import Blueprint, render_template


from . import model

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    user = model.User(1, "mary@example.com", "mary")
    posts = [
        model.Message(
            1, user, "Test post", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            2, user, "Another post", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            3, user, "Custom post", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    return render_template("main/index.html", posts=posts)


@bp.route("/profile")
def user():
    user = model.User(1, "mary@example.com", "mary")
    user.photo =  default.PHOTO
    posts = [
        model.Message(
            1, user, "Test post", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            2, user, "Another post", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            3, user, "Custom post", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    return render_template("main/profile.html", user=user, posts=posts)

@bp.route("/messages")
def messages():
    user = model.User(1, "mary@example.com", "Marie")
    users = [model.User(i+2, name + '@example.com', name) for i, name in zip(range(4), ['emilio', 'pablo', 'rosa', 'hilda'])]


    message = model.Message(
            1, user, "I am testing if this awsome page works", datetime.datetime.now(dateutil.tz.tzlocal())
        )

    replies = [model.Message(i+2, 
                users[i],
                text,
                datetime.datetime.now(dateutil.tz.tzlocal())) for i, text in zip(range(4), ['coll', 'great', 'rt', 'love you'])]
    return render_template("main/message.html", post = message, user = user, n_replies = len(replies), replies =replies)