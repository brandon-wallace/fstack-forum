# application/forum/routes.py

# import os
# from PIL import Image
# from datetime import datetime
from flask import (Blueprint, render_template, url_for,
                   flash, redirect, request, abort)
from sqlalchemy.exc import IntegrityError
from application import db, bcrypt
from application.forms import (SignUpForm, LoginForm, UpdateAccountForm,
                               CreatePostForm, UpdatePostForm, CommentForm)
from application.models import User, Post, Comment
from flask_login import login_user, logout_user, login_required, current_user
from application.decorators import check_email_confirmation

forum = Blueprint('forum', __name__)


@forum.route('/')
def index():
    '''Landing page'''

    # posts = Post.query.order_by(Post.date_posted.desc()).limit(4).all()
    posts = Post.query.all()
    # comments = Comment.query.filter(Comment.post_id == posts.id).count()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=3)
    # return render_template('forum/index.html', posts=posts, comments=comments)
    return render_template('forum/index.html', posts=posts)


@forum.route('/forum', methods=['GET'])
@login_required
@check_email_confirmation
def forum_route():
    '''Forum route'''

    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=4)
    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    content = {
            'image_file': profile_image,
            'posts': posts
            }
    return render_template('forum/forum.html', **content)


@forum.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    '''Create new post route'''

    form = CreatePostForm(category='general')
    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    if form.validate_on_submit():
        try:
            post = Post(title=form.title.data, category=form.category.data,
                        content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            db.session.remove()
            flash('Post created successfully', 'success')
            return redirect(url_for('forum.create_post'))
        except IntegrityError:
            db.session.rollback()
            flash('Post not successful', 'fail')
            return redirect(url_for('forum.forum_route'))
    content = {
            'image_file': profile_image,
            'page_title': 'New',
            'form': form,
            'post': None
            }
    return render_template('forum/create_post.html', **content)


@forum.route('/post/<int:post_id>', methods=['GET', 'POST'])
def display_post(post_id):
    '''Display user posts'''

    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post_id).all()

    if form.validate_on_submit():
        try:
            comment = Comment(content=form.content.data, post_id=post_id,
                              author=current_user)
            db.session.add(comment)
            db.session.commit()
            # db.session.remove()
            flash(' Your comment has been posted.', 'success')
            return redirect(url_for('forum.display_post', post_id=post.id))
        except IntegrityError:
            flash(' Your comment has not been posted.', 'fail')
            db.session.rollback()
            return redirect(url_for('forum.display_post',
                            form=form, post_id=post.id))
    content = {
            'post': post,
            'form': form,
            'comments': comments
            }
    return render_template('forum/post.html', **content)


@forum.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    '''Update a post'''

    post = Post.query.get_or_404(post_id)
    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(' Your post has been updated', 'success')
        return redirect(url_for('forum.display_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    content = {
            'image_file': profile_image,
            'page_title': 'Update',
            'form': form,
            'post': post
            }
    return render_template('forum/update.html', **content)


@forum.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    '''Update a post'''

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    db.session.remove()
    flash(' Your post has been deleted', 'success')
    return redirect(url_for('forum.forum_route'))


@forum.route('/about')
def about():
    '''About page'''

    return render_template('forum/about.html')


@forum.route('/feedback')
def feedback():
    '''Feedback route'''

    posts = Post.query.filter_by(category='feedback')
    return render_template('forum/feedback.html', posts=posts)


@forum.route('/help')
def help():
    '''Help route'''

    posts = Post.query.filter_by(category='help')
    return render_template('forum/help.html', posts=posts)


@forum.route('/html-css')
def html_css():
    '''HTML CSS route'''

    posts = Post.query.filter_by(category='html-css')
    return render_template('forum/html-css.html', posts=posts)


@forum.route('/javascript')
def javascript():
    '''Javascript route'''

    posts = Post.query.filter_by(category='javascript')
    return render_template('forum/javascript.html', posts=posts)


@forum.route('/general')
def general():
    '''General route'''

    posts = Post.query.filter_by(category='general')
    return render_template('forum/general.html', posts=posts)


@forum.route('/nodejs')
def nodejs():
    '''Nodejs route'''

    posts = Post.query.filter_by(category='nodejs')
    return render_template('forum/nodejs.html', posts=posts)


@forum.route('/support')
def support():
    '''Support route'''

    posts = Post.query.filter_by(category='support')
    return render_template('forum/support.html', posts=posts)


@forum.route('/python')
def python():
    '''Python route'''

    posts = Post.query.filter_by(category='python')
    return render_template('forum/python.html', posts=posts)


@forum.app_errorhandler(404)
def page_not_found(error):
    '''Page not found'''

    return render_template('404.html'), 404


@forum.app_errorhandler(403)
def forbidden(error):
    '''Access denied'''

    return render_template('403.html'), 403


@forum.app_errorhandler(500)
def internal_server_error(error):
    '''Internal server error'''

    return render_template('500.html'), 500
