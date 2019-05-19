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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
       
    def __init__(self, title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref = 'owner')
   
    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')




@app.route('/login', methods= ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect ('/newpost')

        elif  user and user.password != password:
            #TODO - explain why login failed
            flash('Incorrect password')
        else:
            if not user:
                flash('User does not exist')
                return redirect ('/login')
        
    return render_template('login.html')
@app.route('/register', methods =['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        #TODO validate data
        username_error = ""
        password_error = ""
        verify_error = ""
        
        
        if not username:
            username_error = "Please enter a username"
        
        elif len(username)>20 or len(username)<3:
            username_error = "Username must be between 3 and 20 characters"
               

        else:
            hasSpace = False
            for char in username:
                if char.isspace():
                    hasSpace = True            
            if hasSpace:
                username_error = "Username cannot contain spaces"        
        

        
        if not password:
            password_error = "Please enter a password"
        
        elif len(password)>20 or len(password)<3:
            password_error = "Password must be between 3 and 20 characters"
               

        else:
            hasSpace = False
            for char in password:
                if char.isspace():
                    hasSpace = True            
            if hasSpace:
                password_error = "Password cannot contain spaces"
                
        if verify != password:
            verify_error = "Passwords must match"
        
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user and not verify_error and not password_error and not username_error:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

        elif existing_user:
            flash('User already exists')    
        else:
            
            #TODO use better respomse messaging
            return render_template('register.html',username_error=username_error,password_error=password_error,verify_error=verify_error)

    return render_template('register.html')


@app.route('/logout')
def logout():
    del session['username']
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