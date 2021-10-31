import datetime
import dateutil.tz
from . import model, default, db

from flask import Blueprint, render_template, request, url_for, redirect,\
    abort
import flask_login

bp = Blueprint("main", __name__)

#---------------------------Home-------------------------------------
@bp.route("/")
@flask_login.login_required
def index():
    posts = model.Message.query.order_by(model.Message.timestamp.desc()).limit(10).all()
    return render_template("main/index.html", current_user=flask_login.current_user, posts=posts)


@bp.route("/profile/<int:user_id>")
@flask_login.login_required
def profile(user_id):
    user = model.User.query.filter_by(id=user_id).first_or_404()
    user.photo =  default.PHOTO
    posts = model.Message.query.filter_by(user=user).order_by(model.Message.timestamp.desc()).all()
    return render_template("main/profile.html", user=user, posts=posts)

@bp.route("/message/<int:message_id>")
@flask_login.login_required
def message(message_id):
    message = model.Message.query.filter_by(id=message_id).first_or_404()
    users = [model.User(email= name+ "@example.com", name= name)\
         for name in ['emilio', 'pablo', 'rosa', 'hilda']]

    """ 
    message = model.Message(
            user = user,
            text = "Why i think we live in a parties dictatorship: \
                We do not select governors, we select parties who decide \
                who the govenors are.", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        )
    """
    replies = [model.Message(
            user = users[i],
            text = text, 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ) for i, text in zip(range(4), ['coll', 'great', 'rt', 'love you'])]
    return render_template("main/message.html",
        post = message,
        n_replies = len(replies), 
        replies =replies)

#---------------------- New Post------------------------------
@bp.route('/new')
@flask_login.login_required
def new():
    return render_template("main/new.html")

@bp.route('/new', methods=['POST'])
@flask_login.login_required
def main_new_post():
    content = request.form.get('new_post')

    post = model.Message(
        user=flask_login.current_user,
        text=content,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('main.post', message_id=post.id))

@bp.route('/post/<int:message_id>')
@flask_login.login_required
def post(message_id):
    post = model.Message.query.filter_by(id=message_id).first_or_404()
    """
    NOT NEEDED BECAUSE OF first_or_404
    if not message:
        abort(404, 'Post id {} does not exist'.format(message_id))"""
    return render_template("main/post.html", post=post)