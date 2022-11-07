"""
Foo Bar:: Ameer Alnasser, Wan Ying Li, Kevin Wang
SoftDev
k19 -- username/password authentication
2022-11-05
time spent: 1.0 hrs
"""

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

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

@app.route('/blog')
def blog():
    return render_template(blog_title = "hi", author="me", )
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
