from flask import Flask,render_template,url_for

app=Flask(__name__)

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

if __name__=="__main__":
    app.run(debug=True) 