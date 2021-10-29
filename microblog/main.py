import datetime
import dateutil.tz
from . import default

from flask import Blueprint, render_template


from . import model

bp = Blueprint("main", __name__)


@bp.route("/")
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
def user():
    user = model.User(email= "mary@example.com", name= "mary")
    user.photo =  default.PHOTO
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
    return render_template("main/profile.html", user=user, posts=posts)

@bp.route("/messages")
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