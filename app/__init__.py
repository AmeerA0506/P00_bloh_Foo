"""
Foo Bar:: Ameer Alnasser, Wan Ying Li, Kevin Wang
SoftDev
P00 
2022-11-05
time spent: 1.0 hrs
"""

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from datetime import datetime
from flask import session, redirect, url_for
import sqlite3   #enable control of an sqlite database

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

# START of username/password authentication -------------------------------------------------------------------------------
CORRECT_username="lol"
CORRECT_password="lol"

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session: #ensure the user isn't already signed in
        #to avoid KeyError if session["username"] doesn't exist
        print(f"the current user is {session['username']}")
        return render_template("response.html", username=session["username"], logged_in=True)
    else:
        print("there is no current user")
        return render_template("response.html", logged_in=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #when submitting the form
        #username is case-unsensitive and password is case-sensitive
        if (CORRECT_username.lower() == request.form["username"].lower() and CORRECT_password == request.form["password"]): #username/password auth
            session['username'] = request.form['username']
            print(f"the current user is {session['username']}")
            return redirect(url_for('index'))
        #when username/password combo is wrong
        elif (CORRECT_username.lower() != request.form["username"].lower()):
            return render_template("login.html", username = request.form["username"], error_message="user doesn't exist")
        elif (CORRECT_username.lower() == request.form["username"].lower() and CORRECT_password != request.form["password"]):
            return render_template("login.html", username = request.form["username"], error_message="incorrect password")
        else:
            return render_template("login.html", username = request.form["username"], error_message="juju madness")  
        
    else: #when accessing /login for the first time
        if 'username' in session: #ensure the user isn't already signed in
            return redirect(url_for('index'))
        else:
            return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
# END of username/password authentication ------------------------------------------------------------------------------------------

# START of database creation-------------------------------------------------------------------------------------------------------
DB_FILE="blog_backend.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

db.execute("DROP TABLE if exists blogs;")
db.execute("DROP TABLE if exists authentication;")
# function(s) to initialize DB 
c.execute("CREATE TABLE blogs(username text, title text, blog text, timestamp text);")
c.execute("CREATE TABLE authentication(username text, password text);")
c.execute("""INSERT INTO blogs VALUES ("kevin", "kevin's first blog", "hi, this is my first blog but oldest version. I'm like really cool and stuff", "2022-11-14 13:45:59.908057");""")
c.execute("""INSERT INTO blogs VALUES ("kevin", "kevin's first blog", "hi, this is my first blog but second oldest version. I'm like really cool and stuff", "2022-12-14 13:45:59.908057");""")
c.execute("""INSERT INTO blogs VALUES ("kevin", "kevin's first blog", "hi, this is my first blog. I'm like really cool and stuff. i just edited this", "2022-12-15 13:45:59.908057");""")
c.execute("""INSERT INTO blogs VALUES ("kevin", "kevin's second blog", "hi, this is my second blog. I'm like really cool and stuff", "2022-12-15 13:45:59.908057");""")
c.execute("""INSERT INTO blogs VALUES ("kevin", "kevin's third blog", "hi, this is my third blog. I'm like really cool and stuff", "2022-12-15 13:45:59.908057");""")
c.execute("""INSERT INTO blogs VALUES ("Ameer", "AA's first blog", "I wish i was as cool as kevin", "2022-12-15 13:45:59.908057");""")
c.execute("""INSERT INTO blogs VALUES ("WanYing", "Wan Ying's first blog", "I wish i was as cool as kevin", "2022-12-15 13:45:59.908057");""")
c.execute("""SELECT * FROM blogs WHERE username = "kevin" AND title = "kevin's first blog";""")

db.commit() #save changes
#END of database creation---------------------------------------------------------------------------------------------------------------

# create blog
# Q: how to get username & timestamp
@app.route('/create', methods=['GET', 'POST'])
def create():
    # check if the user is logged in
    if 'username' not in session:
        return render_template("response.html", logged_in=False)

    # when users submitted their blog
    if request.method == 'POST': 
        # add newly created blog to BLOGS db
        #print(f'INSERT INTO BLOGS VALUES("{session["username"]}", "{request.form["blog_title"]}", "{request.form["content"]}", {datetime.now()});')
        c.execute(f'INSERT INTO BLOGS VALUES("{session["username"]}", "{request.form["blog_title"]}", "{request.form["content"]}", "{datetime.now()}");')   
        #c.execute("SELECT * FROM BLOGS;")
        #print(c.fetchall())
        return redirect(url_for('blog', author=session["username"], title=request.form["blog_title"]))
    else:
        return render_template("create.html")

# edit blog
@app.route('/blog/<string:author>/<string:title>/edit', methods=['GET', 'POST'])
def edit(author, title):
    # check if the user is logged in
    if 'username' not in session:
        return render_template("response.html", logged_in=False)

    # check if user is blog owner 
    if session["username"] != author:
        return "You don't have access to edit this page because you are not the author."  
        
    # when users submitted their blog
    if request.method == 'POST': 
        # add newly created blog to BLOGS db
        c.execute(f'INSERT INTO blogs VALUES("{session["username"]}", "{title}", "{request.form["content"]}", "{datetime.now()}");')
    
    return render_template("edit.html", blog_title = title, author = session["username"])

# directory page
@app.route('/directory')
def directory():
    #c.execute(f'.mode box')
    print(c.execute(f'SELECT * FROM blogs;'))  
    return render_template("directory.html")

# blog page
@app.route('/blog/<string:author>/<string:title>')
def blog(author, title):
    c.execute(f'SELECT * FROM blogs WHERE username = "{author}" AND title = "{title}" ORDER BY timestamp DESC LIMIT 1;')
    #print(c.fetchone())
    content, timestamp = c.fetchone()[2:4]
    return render_template("blog.html", blog_title = title, author = author, timestamp=timestamp, content=content)

# blog hisotry page    
@app.route("/blog/<string:author>/<string:title>/history/page/<int:page>")
def blog_history(author, title, page):
    c.execute(f'SELECT * FROM blogs WHERE username = "{author}" AND title = "{title}" ORDER BY timestamp DESC LIMIT -1 OFFSET 1;')
    old_blogs = c.fetchall()
    if (old_blogs):
        return render_template(
            "blog_history.html",
            blog_title = title,
            author = author, 
            timestamp = old_blogs[page-1][3],
            content = old_blogs[page-1][2],
            page_number = page,
            is_last_page = page == len(old_blogs)
        ) 
    else:
        return "No history found"


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    #app.debug = True 
    app.run()
    db.close()  #close database
