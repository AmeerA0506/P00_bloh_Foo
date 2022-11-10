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

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

# START of username/password authentication -------------------------------------------------------------------------------
CORRECT_username="lol"
CORRECT_password="lol"

from flask import session, redirect, url_for

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

'''
import sqlite3   #enable control of an sqlite database
DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# function(s) to initialize DB 


db.commit() #save changes
db.close()  #close database
'''
# create blog
# Q: how to get username & timestamp
@app.route('/create')
def create():
    # check if the user is logged in
    if 'username' not in session:
        return render_template("response.html", logged_in=False)
        
    # when users submitted their blog
    if request.method == 'POST': 
        # add newly created blog to BLOGS db
        c.execute(f'INSERT INTO BLOGS VALUES("{username}", "{request.form["title"]}", "{request.form["content"]}", {timestamp});')
    
    return render_template("create.html", blog_title = title, content = content, timestamp = "11/11/23 5:32:53", author = username)

# edit blog
@app.route('/edit')
def edit(content):
    # check if the user is logged in
    if 'username' not in session:
        return render_template("response.html", logged_in=False)

    # check if user is blog owner 
    
        
    # when users submitted their blog
    if request.method == 'POST': 
        # add newly created blog to BLOGS db
        c.execute(f'INSERT INTO BLOGS VALUES("{username}", {title}, {request.form["content"]}, {timestamp});')
    
    return render_template("edit.html", blog_title = title, content = content, timestamp = "11/11/23 5:32:53", author = username)

# blog page
@app.route('/blog/<string:author>/<string:title>')
def blog(author, title):
    return render_template("blog.html", blog_title = title, author = author, timestamp="11/11/23 5:32:53", content="lorem ipsum")

# blog hisotry page    
@app.route("/blog/<string:author>/<string:title>/history/page/<int:page>")
def blog_history(author, title, page):
    same_blogs_different_versions_by_timestamp = [
        #[timestamp, content]
        ["11/9/23 5:32:53", "lorem ipsum 1"],
        ["11/8/23 5:32:53", "lorem ipsum 2"],
        ["11/7/23 5:32:53", "lorem ipsum 3"]
    ]
    print(page)
    return render_template(
        "blog_history.html",
        blog_title = title,
        author = author, 
        timestamp = same_blogs_different_versions_by_timestamp[page-1][0],
        content = same_blogs_different_versions_by_timestamp[page-1][1],
        page_number = page,
        is_last_page = page == len(same_blogs_different_versions_by_timestamp)
    ) 


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
