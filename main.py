from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:denise@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))

    def __init__(self,title,body):
        self.title = title
        self.body = body


@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    if request.method == "POST":
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title,blog_body)
        db.session.add(new_blog)
        db.session.commit()
     
    blogs = Blog.query.filter_by(id=id)
    
    return render_template('newpost.html',title="Build A Blog!",blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        blog_title = request.form['title']
        new_blog = Blog(blog_title)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(id=id)
    
    return render_template('blog.html',title="Build A Blog!",blogs=blogs) 
       





if __name__ == '__main__':
    app.run()