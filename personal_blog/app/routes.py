from app import app
from flask import render_template, flash, redirect, url_for, request, abort
from app.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post
from urllib.parse import urlsplit
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html',  title='Home', posts=posts)

@app.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', title='blog',posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get(int(post_id))
    if post:
        return render_template('post.html', post=post)
    else:
        return "Post not found", 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


"""Admin routes"""
@app.route('/bamiboy', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    posts = Post.query.all()
    form = PostForm()
    return render_template('admin.html', title = 'admin', posts=posts, post_form=form)

@app.route('/admin/save_post', methods=['POST'])
@login_required
def save_post():
    form = PostForm()
    if form.validate_on_submit():
        if request.args.get('post_id'):  # Editing an existing post
            post = Post.query.get(request.args.get('post_id'))
            post.title = form.title.data
            post.content = form.content.data
            flash('Post updated successfully!', 'success')
        else:  # Creating a new post
            new_post = Post(title=form.title.data, content=form.content.data)
            db.session.add(new_post)
            flash('Post created successfully!', 'success')
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/edit/<int:post_id>')
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():  # Handle form submission for editing
        post.title = form.title.data
        post.body = form.content.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('admin.html', posts=Post.query.all(), post_form=form)

@app.route('/admin/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        abort(403)
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin'))