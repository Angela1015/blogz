from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:denise@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))
       
    def __init__(self, title,body):
        self.title = title
        self.body = body
      

@app.route('/newpost', methods=['POST', 'GET'])

def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_blog = Blog(blog_title, blog_body)
        blog_title_error = ''
        blog_body_error = ''
   
        if not blog_title:
            blog_title_error = "Please complete this field" 
            blog_title = ""
           
            

        if not blog_body:
            blog_body_error = "Please complete this field"
            blog_body = ""

        if not blog_title_error and not blog_body_error:
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog") 
        else:
    
            return render_template('newpost.html',title="Build A Blog!",blog_title_error ="Please complete this field",blog_body_error ="Please complete this field")
@app.route ('/blog', methods = ['POST','GET'] )
def blog():
        
    blogs = Blog.query.all()
    
    return render_template('blog.html',title="Build A Blog!", 
        blogs=blogs)


if __name__ == '__main__':
    app.run()
    #trying to mess up github
    #trying to mess up github againfrom flask import Flask, request, redirect, render_template