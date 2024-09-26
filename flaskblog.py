from flask import Flask,render_template,url_for
from forms import RegistrationForm,LoginForm

app=Flask(__name__)
app.config['SECRET_KEY']='c9eaf8c09505025481a9ba1faa0fb1dd'

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
def hello():
    return render_template('home.html',posts_value=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register")
def register():

    # creating instance of registration form 
    form=RegistrationForm() 
    return render_template('register.html',title='Register',form=form)


@app.route("/login")
def login():

    # creating instance of registration form 
    form=RegistrationForm() 
    return render_template('login.html',title='login',form=form)

if __name__=="__main__":
    app.run(debug=True) 