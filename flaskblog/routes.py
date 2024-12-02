import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash ,redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm,LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html',posts_value=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # creating instance of registration form 
    form=RegistrationForm() 
    if form.validate_on_submit():
        #generating hash for password and converting it to string from byte using decode utf-8
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #creating instance of user
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() #adding user to database
        flash(f"Your account has been created . You are now able to Log in !", 'success') 
        # here success is the category of flash message 
        return redirect(url_for('login'))

    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # creating instance of login form 
    form=LoginForm() 
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data) #we will log the user in once email and password is verified
            next_page=request.args.get('next') #for redirects
            print("next page : ",next_page)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        
        else:
            flash("Login Unsuccessful. Please check username and password ","danger")
        
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user() #no need to pass any arguments as this function already knows what user is logged in currently
    return redirect(url_for('home'))

def save_picture(form_picture):
    #to create random name of picture
    random_hex = secrets.token_hex(8) 
    f_name, f_extension= os.path.splitext(form_picture.filename) #form_picture is data from field which user submits, the name fo the file.
    picture_fn= random_hex + f_extension #final file name 
    picture_path= os.path.join(app.root_path, 'static/profile_pics', picture_fn) #path where image need to be saved
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #saving th picture 

    return picture_fn


@app.route("/account",methods=['GET','POST'])
@login_required #adding this decorator so that only when a user is logged in he can see the account page, to tell where to look for login route we will specify in init.py
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET': #form will populate data with current username and mail
        form.username.data = current_user.username
        form.email.data= current_user.email
    
    image_file=url_for('static', filename='profile_pics/' + f"{current_user.image_file}")
    return render_template('account.html',title='Account', image_file= image_file, form=form)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id) #returns 404 if id does not exist
    return render_template('post.html', title=post.title, post = post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 forbideen route
    form = PostForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content= form.content.data
        db.session.commit() #as we are updating existing data , no need to db.session.add
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method== 'GET':
        form.title.data = post.title #populating the update post link with existing post data
        form.content.data= post.content
    return render_template('create_post.html', title="Update_Post" , form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 forbideen route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))