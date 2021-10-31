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
    posts = (model.Message
                .query.filter_by(response_to=None)
                .order_by(model.Message.timestamp.desc())
                .limit(10).all())
    return render_template("main/index.html", current_user=flask_login.current_user, posts=posts)


@bp.route("/profile/<int:user_id>")
@flask_login.login_required
def profile(user_id):
    user = model.User.query.filter_by(id=user_id).first_or_404()
    user.photo =  default.PHOTO
    posts = (model.Message
                    .query.filter_by(response_to=None)
                    .filter_by(user=user).order_by(model.Message.timestamp.desc())
                    .all())
    return render_template("main/profile.html", user=user, posts=posts)

@bp.route("/message/<int:message_id>")
@flask_login.login_required
def message(message_id):
    message = model.Message.query.filter_by(id=message_id).first_or_404()
    if not message.response_to:
        replies = model.Message.query.filter_by(response_to_id=message_id).all()
        return render_template("main/message.html",
            post = message,
            n_replies = len(replies), 
            replies =replies)
    abort(403)

#---------------------- New Post------------------------------
@bp.route('/new')
@flask_login.login_required
def new():
    return render_template("main/new.html")

@bp.route('/new', methods=['POST'])
@flask_login.login_required
def main_new_post():
    message_id = request.form.get('response_to')
    if message_id:
        message = model.Message.query.filter_by(id = message_id).first_or_404()
    else:
        message = None
    content = request.form.get('new_post')
    post = model.Message(
        user=flask_login.current_user,
        text=content,
        response_to=message,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )
    db.session.add(post)
    db.session.commit()
    if message_id:
        return redirect(url_for('main.post', message_id=message_id))
    return redirect(url_for('main.post', message_id=post.id))

@bp.route('/post/<int:message_id>')
@flask_login.login_required
def post(message_id):
    post = model.Message.query.filter_by(id=message_id).first_or_404()
    responses = model.Message.query.filter_by(response_to_id = post.id).order_by(model.Message.timestamp.desc()).all()
    """
    NOT NEEDED BECAUSE OF first_or_404
    if not message:
        abort(404, 'Post id {} does not exist'.format(message_id))"""
    return render_template("main/post.html", post=post, n_replies = len(responses), replies=responses)

#---------------------------Follows----------------------------------------
@bp.route("/follow/<int:user_id>", methods=['POST'])
@flask_login.login_required
def follow(user_id):
    followed = model.User.query.filter_by(id = user_id).first_or_404()

    if user_id == current_user.user_id:
        abort(403, "Cannot follow yourself")
    if user in current_user.following:
        abort(403, 'User already followed')
    
    current_user.following.append(followed)
    db.session.commit()
    return redirect(url_for('main.profile', user_id=user_id))

@bp.route("/unfollow/<int:user_id>", method=['POST'])
@flask_login.login_required
def unfollow(user_id):
    user = model.User.query.filter_by(id=user_id).first_or_404()
    if user in current_user.following:
        user_to_remove = current_user.following.remove(user_to_remove)
    return redirect(url_for('main.profile', user_id=user_id))
    