from flask import render_template,url_for,flash ,redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog.models import User, Post

posts=[
    {
    'author':'B V Lakshmi',
    'title':'My daily routine',
    'date_posted':'April 26th 2009',
    'content':'The day my life changed completely by Lakshmi'
    },
    {
    'author':'Divya',
    'title':'Stocks to watch out for ',
    'date_posted':'June 12 2005',
    'content':'These stocks are too good to be true!'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts_value=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register", methods=['GET','POST'])
def register():

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
    # creating instance of login form 
    form=LoginForm() 
    if form.validate_on_submit():
        if form.email.data=='admin@blog.com' and form.password.data=='Password':
            flash("You have been logged In !","success")
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check username and password ","danger")
        
    return render_template('login.html',title='Login',form=form)
