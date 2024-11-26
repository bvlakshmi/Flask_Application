from datetime import datetime
from flaskblog import db

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg') #we are going to hash the image files that are 20 characters long so they all are unique
    password=db.Column(db.String(60),nullable=False)
    #posts attribute has a relationship with Post model , backerf is similar to adding another column to the Post Model, backref allows us when we have a post we can use author attribute to see the user who created the post.
    #lazy attribute, when sql alchemy loads the data from the database, true means data is loaded in one go . With this relationship we will be able to use this post attribute to fetch all the posts written by a author.
    posts=db.relationship('Post', backref='author', lazy=True)

    #dunder method or magic method, to represent how out object is printed
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    #if date not specified , default value will be current date
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.now)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #user.id is table user and id is the column in the table.

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"