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
    name = db.Column(db.String(120))
    blog_content = db.Column(db.String(240))
    completed = db.Column(db.Boolean)
    
    def __init__(self, name,blog_content):
        self.name = name
        self.completed = False
        self.blog_content=blog_content
       

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_name = request.form['blog_title']
        blog_content = request.form['blog_content']
        new_blog = Blog(blog_name, blog_content)

        if not blog_name:           
                flash("This field must be completed")

        elif not blog_content:
                 flash("This field must be completed")                  

        if blog_content and blog_name:                                  
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog")
                
    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('newpost.html',title="Build A Blog!", 
        blogs=blogs, completed_blogs=completed_blogs)

@app.route ('/blog', methods = ['POST','GET'] )
def blog():
    
    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        
        db.session.add(new_blog,new_blog_content)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build A Blog!", 
        blogs=blogs, completed_blogs=completed_blogs)

@app.route ('/individualblog', methods= ['GET'])
def individualblog():
    if request.method == "GET":
        
        blog_name = name
        blog_content = blog_content   
        individualblog=request.args.get('individualblog')
    return render_template('individualblog.html',blog_content=blog_content,blog_name=blog)

if __name__ == '__main__':
    app.run()
    #trying to mess up github
    #trying to mess up github againfrom flask import Flask, request, redirect, render_template