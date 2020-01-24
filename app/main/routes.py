from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Post, Comment
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
   post = Post.query.order_by(Post.id.desc()).all()
   return render_template('index.html', title="Home", posts=post)
