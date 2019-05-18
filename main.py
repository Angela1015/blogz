from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:denise@localhost:8889/blogz'
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

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
   
    def __init__(self,email,password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')




@app.route('/login', methods= ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect ('/newpost')
        else:
            #TODO - explain why login failed
            return '<h1>error!<h1>'
        
    return render_template('login.html')
@app.route('/register', methods =['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        #TODO validate data
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email,password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
        else:
            
            #TODO use better respomse messaging
            return "<h1>DUPLICATE USER<h1>"

    return render_template('register.html')


@app.route('/logout')
def logout():
    del session['email']
    return redirect ('/blog')

@app.route('/newpost')

def newpost():


    return render_template('newpost.html',title = "Add A Blog")

@app.route('/newpost', methods = ['POST','GET'])
def add_newpost():        
    if request.method == "POST":
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_blog = Blog(blog_title, blog_body)
        blog_title_error = ''
        blog_body_error = ''
    
        if not blog_title:
            blog_title_error="Please complete this field."
            #blog_title_error=""
            
                        
        if not blog_body:
            blog_body_error="Please complete this field."
           # blog_body_error=""
           

        if blog_title and blog_body:
            #new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)  
            db.session.commit()  
            url = "/blog?id="+str(new_blog.id)
            return redirect(url)
        else:    
            return render_template('newpost.html',title="Add A Blog!",blog_title_error=blog_title_error,blog_body_error=blog_body_error,blog_title=blog_title,blog_body=blog_body)
        
            
        

       #
    return render_template('newpost.html',title = "Add A Blog!")
            
@app.route ('/blog', methods = ['POST','GET'] )
def blog():
   
    blog_id = request.args.get('id')
    if not blog_id:    
        blogs = Blog.query.all()
        
        return render_template('blog.html',title="Build A Blog!",blogs=blogs) 
    
    else:
        blog = Blog.query.get(blog_id)
        return render_template('individualblog.html',title="Build A Blog",blog=blog)

       

if __name__ == '__main__':
    app.run()
    #trying to mess up github
    #trying to mess up github againfrom flask import Flask, request, redirect, render_template