from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.config['SECRET_KEY']='c9eaf8c09505025481a9ba1faa0fb1dd'
# will create a site.db file in the current directory 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#Creating database instance 
db= SQLAlchemy(app)
#with SQLalchemy we can represent our database structures as classes 

bcrypt=Bcrypt(app)

#importing routers after creating db instance to avoid circular import errors.
from flaskblog import routes