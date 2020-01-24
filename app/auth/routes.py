from flask import render_template, flash, redirect, url_for, request
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, CreatePostForm, DeletePostForm, UpdatePostForm, AddCommentForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Post, Comment


@bp.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for("main.index"))
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user is None or not user.check_password(form.password.data):
         flash('Invalid username or password')
         return redirect(url_for('auth.login'))
      elif user == "admin" and user.check_password(form.password.data, "admin"):
         flash('Welcome Admin!')
      else:
         flash("Welcome {}".format(user.username))
      login_user(user, remember=form.remember.data)
      return redirect(url_for("main.index"))
   return render_template('login.html', title="Login", form=form)

@bp.route('/logout')
def logout():
   logout_user()
   return redirect(url_for("main.index"))

@bp.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for("main.index"))
   form = RegistrationForm()
   if form.validate_on_submit():
      user = User(name = form.name.data, username = form.username.data, email = form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash("Registration issa success!")
      return redirect(url_for('auth.login'))
   return render_template('register.html', title="Register", form=form)

@bp.route('/create_post', methods=['GET', 'POST'])
def create_post():
   if not current_user.is_authenticated:
      return redirect(url_for('auth.login'))
   article = CreatePostForm()
   if article.validate_on_submit():
      post = Post(title = article.title.data, body = article.content.data, author = current_user)
      db.session.add(post)
      db.session.commit()
      flash("New article created")
      return redirect(url_for("main.index"))
   return render_template('create_post.html', title="New Article", form=article)

@bp.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
   if current_user.username != "admin":
      flash("Sorry, the Admin is the only person authorized for this operation")
      return redirect(url_for("main.index"))
   form = DeletePostForm()
   if form.validate_on_submit():
      # get the particular post in question, alongside all associated comments with it and perform
      # the db.session.delete action whilst committing at the end to ensure the changes are effected
      post = Post.query.filter_by(title=form.title.data).first()
      comments = Comment.query.filter_by(article=post).all()
      db.session.delete(post)
      db.session.commit()
      for comment in comments:
         db.session.delete(comment)
         db.session.commit()
      flash("Article has been deleted")
      return redirect(url_for("main.index"))
   return render_template('delete_post.html', title="Delete", form=form)

@bp.route('/update_post/<id>', methods=['GET', 'POST'])
def update_post(id):
   if current_user.username != "admin":
      flash("Sorry, the Admin is the only person authorized for this operation")
      return redirect(url_for("main.index"))
   form = UpdatePostForm()
   # get the particular post by it's id, also get all comments associated with it, and the user who wrote such
   # post. Next, on updating the post, first delete-commit the post, the get the updated post contents (title, body
   # and author reference). Add-commit the new post the loop through the already extracted comments and reassign their
   # 'article' references to the current post. Finally, add-commit each of them before redirecting.
   get_post = Post.query.filter_by(id=id).first_or_404()
   get_post_comment = Comment.query.filter_by(article=get_post).all()
   user_who_wrote = get_post.author
   if form.validate_on_submit():
      db.session.delete(get_post)
      db.session.commit()
      updated_post = Post(title = form.title.data, body = form.update.data, author = user_who_wrote)
      db.session.add(updated_post)
      db.session.commit()
      for comments in get_post_comment:
         comments.article = updated_post
      db.session.add(comments)
      db.session.commit()
      flash("Article has been Updated")
      return redirect(url_for("main.index"))
   elif request.method == 'GET':
      form.title.data = get_post.title
      form.update.data = get_post.body
   return render_template('update_post.html', title="Update", form=form)

@bp.route('/article/<title>', methods=['GET', 'POST'])
def article(title):
   post = Post.query.filter_by(title=title).first_or_404()
   user = User.query.all()
   commentform = AddCommentForm()
   if commentform.validate_on_submit():
      # Below, the 'commentform.' in the db query is commentform = AddCommentForm(); from above.
      # The second comment is the name of the field of the comment form from whence its data
      # being rendered as a form in the html is obtained as assigned to the Comments table
      comments = Comment(saying=commentform.comment.data, author=current_user, article=post)
      db.session.add(comments)
      db.session.commit()
      commentform.comment.data = ""
   dbcomments = Comment.query.filter_by(article=post).order_by(Comment.comment_tmestp.desc()).all()
   return render_template('article.html', post=post, addcomment=commentform, dbcomments=dbcomments)
