from flaskblog import db, app
app.app_context().push()
# db.create_all()
from flaskblog.models import User,Post
print(User.query.all())
user=User.query.first()
print(user)
print(user.password)
print(Post.query.all())
# user_1=User(username='Corey', email='C@demo.com', password='password')
# db.session.add(user_1)
# user_2=User(username='JohnDoe', email='db@demo.com', password='password') 
# db.session.add(user_2)
# db.session.commit()
# user=User.query.filter_by(username='Corey').first()
# print(User.query.all())
# print(Post.query.all())
# post_1=Post(title='Blog 1 ', content='First post content!',user_id=user.id)
# db.session.add(post_1)
# db.session.commit()
# post_2=Post(title='Blog 2 ', content='Second post content!',user_id=user.id) 
# db.session.add(post_2)
# db.session.commit()
# print(Post.query.all())
# for post in user.posts:
#     print(post.title)
# post=Post.query.first()
# print(post)
# print(post.author)
# db.drop_all()