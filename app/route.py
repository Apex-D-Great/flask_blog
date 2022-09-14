from flask import render_template, flash, request, redirect, url_for
from app.webforms import SearchForm, Register, PostForm, Login, Form, DashForm, AdminForm
from app.model import User, Post
from flask_login import login_user, login_required, current_user, logout_user
from app import db, app
from werkzeug.utils import secure_filename
import uuid as uuid
import os

UPLOAD_FOLDER = 'app/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("User Added Successfully")
        login_user(user)
        return redirect(url_for("dashboard"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"there was an error creating user: {err_msg}")
    return render_template("add_user.html", form=form)

@app.route("/add_posts", methods=['GET', 'POST'])
@login_required
def add_posts():
    poster = current_user.id
    form = PostForm()
    if form.validate_on_submit():
        posts = Post(title=form.title.data, poster_id=poster, slug=form.slug.data, content=form.content.data)
        form.title.data = ''
        form.slug.data = ''
        form.content.data = ''
        db.session.add(posts)
        db.session.commit()
        flash("post created successfully")
        return redirect(url_for("posts"))
    return render_template("add_post.html", form=form)

@app.route("/posts")
def posts():
    posts = Post.query.order_by(Post.date_posted)
    return render_template("posts.html", posts=posts)

# individual post
@app.route("/post/<int:id>")
def post(id):
    posts = Post.query.get_or_404(id)
    return render_template("individual_post.html", posts=posts)

@app.route("/post/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    posts = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        posts.title = form.title.data
        posts.slug = form.slug.data
        posts.content = form.content.data
        # add to database
        db.session.add(posts)
        db.session.commit()
        flash("Post Updated Successfully")
        return redirect(url_for("posts"))
    form.title.data = posts.title
    form.slug.data = posts.slug
    form.content.data = posts.content
    return render_template("update.html", form=form)



# dashboards
@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html") 

# update dashboard
@app.route("/dashboard/update", methods=['GET', 'POST'])
@login_required
def update_dashboard():
    id = current_user.id
    form = DashForm()
    user_to_update = User.query.get_or_404(id)
    form.about.data = user_to_update.about
    if request.method == 'POST':
        user = User.query.filter_by(name=form.name.data).first()
        # this first logic is just to prevent updating a username to an existing username
        # how about if user post same name as before, the first logic takes care of that
        # if they updated their about or profile pic alongside then only those two should be updated
        if current_user.name == form.name.data and current_user.email == form.email.data:
            user_to_update.about = request.form['about']
            # if request.files['profile_pic']:
            #     # this is the extracted picture
            #     user_to_update.profile_pic = request.files['profile_pic']
            #     # grab image name and secure filename to prevent sql injection
            #     pic_filename = secure_filename(user_to_update.profile_pic.filename)
            #     # set UUID
            #     pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #     saver = request.files['profile_pic']
            #     user_to_update.profile_pic = pic_name
            #     # save the image in a try/except block in case of any image error
            #     try:
            #         db.session.commit()
            #         saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            #         flash("user updated successfully")
            #         return redirect(url_for('dashboard'))
            #     except:
            #         flash("error! looks like there was a problem")
            #         return render_template('update_dashboard.html', form=form, user_to_update=user_to_update)
            try:
                db.session.commit()
                flash("user updated successfully")
                return redirect(url_for('dashboard'))
            except:
                flash("error! looks like there was a problem")
                return render_template('update_dashboard.html', form=form, user_to_update=user_to_update)
        elif user:
            flash("username/email already exist, try another username/email")
            return render_template('update_dashboard.html', form=form, user_to_update=user_to_update)
        else:
            user_to_update.name = request.form['name']
            user_to_update.email = request.form['email']
            user_to_update.about = request.form['about']
            # if request.files['profile_pic']:
            #     # this is the extracted picture
            #     user_to_update.profile_pic = request.files['profile_pic']
            #     # grab image name and secure filename to prevent sql injection
            #     pic_filename = secure_filename(user_to_update.profile_pic.filename)
            #     # set UUID
            #     pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #     saver = request.files['profile_pic']
            #     user_to_update.profile_pic = pic_name
            #     # save the image in a try/except block in case of any image error
            #     try:
            #         db.session.commit()
            #         saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            #         flash("user updated successfully")
            #         return redirect(url_for('dashboard'))
            #     except:
            #         flash("error! looks like there was a problem")
            #         return render_template('update_dashboard.html', form=form, user_to_update=user_to_update)
            try:
                db.session.commit()
                flash("user updated successfully")
                return redirect(url_for('dashboard'))
            except:
                flash("error! looks like there was a problem")
                return render_template('update_dashboard.html', form=form, user_to_update=user_to_update)
    else:
        return render_template('update_dashboard.html', form=form, user_to_update=user_to_update)


# search route
@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        # get data from the form
        searchs = form.searched.data
        # query the database
        posts = posts.filter(Post.content.like('%' + searchs + '%'))
        posts = posts.order_by(Post.title).all()
        return render_template('search.html', searchs=searchs, posts=posts)

# admin route
@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    id == current_user.id
    if current_user.id == 1:
        return render_template('admin.html')
    else:
        flash('you are not authorized to access this page')
        return redirect(url_for('dashboard'))

# admin search route
@app.route("/admin/search", methods=['GET', 'POST'])
@login_required
def adminsearch():
    form = AdminForm()
    # search = None
    # user = None
    if form.validate_on_submit():
        # get data from the form
        search = form.adminsearch.data
        # query the database
        user = User.query.filter_by(name=search).first()
        if user:
            return render_template('adminsearch.html', search=search, user=user)
        else:
            flash("user doesn't exist")
            return redirect(url_for('admin'))
    # return render_template('adminsearch.html', search=search, user=user)
   
    

# delete user
@app.route("/deleteuser/<int:id>", methods=['GET', 'POST'])
@login_required
def deleteuser(id):
    user_to_be_deleted = User.query.get_or_404(id)
    db.session.delete(user_to_be_deleted)
    db.session.commit()
    return redirect(url_for('admin')) 

# delete post
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete(id):
    userid = current_user.id
    post_to_be_deleted = Post.query.get_or_404(id)
    if userid == post_to_be_deleted.poster.id or userid == 1:
        db.session.delete(post_to_be_deleted)
        db.session.commit()
        flash("post deleted successfully")
        return redirect(url_for("posts"))
    else:
        flash("you are not authorized to carry out this operation...")
        return redirect(url_for("posts"))

# login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(pwd=form.password.data):
            login_user(user)
            flash(f"success! you're logged in")
            return redirect(url_for("dashboard"))
        else:
            flash("username and password mismatch")
    return render_template("login.html", form=form)

# logout route
@app.route('/logout')
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for("login"))

@app.route("/", methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/name", methods=['GET','POST'])
def name():
    name = None
    form = Form() 
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("user created successfully", category="info")
    return render_template("name.html", name=name, form=form)

# @app.route("/update/<id>", methods=['GET', 'POST'])
# def update(id):
#     form = UserForm()
#     user_to_update = User.query.get_or_404(id)
#     if request.method == 'POST':
#         user_to_update.name = request.form['name']
#         user_to_update.email = request.form['email']
#         try:
#             db.session.commit()
#             flash("user updated successfully")
#             return render_template(update.html, form=form, user_to_update=user_to_update)
#         except:
#             flash("error! looks like there was a problem")
#             return render_template(update.html, form=form, user_to_update=user_to_update)
#     else:
#         return render_template(update.html, form=form, user_to_update=user_to_update)

# custom error pages 
 
# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html"), 404

# internal server error
@app.errorhandler(500)
def server_error(e):
    return render_template("error500.html"), 500

