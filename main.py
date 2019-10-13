from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

def username_error(username):
    space = False
    for letter in username:
        if letter.isspace() == True:
            space = True
#def username_error(username): this is from Sai - she wanted me to try this instead
    #for letter in password:
        #if letter.isspace() == True:
            #space = True
        #else:
            #space = False    

    if 3 < len(username) < 20 and space == False :
        return False
    else:
        return True

def password_error(password):
    space = False
    for letter in password:
        if letter.isspace() == True:
            space = True
    
    if 3 <len(password) < 20 and space == False:
        return False
    else:
        return True

def verify_password_error(verify, password):
    if verify == password:
        return False
    else:
        return True

def email_error(email):
    if "@" in email and "." in email and " " not in email and 3 < len(email) < 20 and email.count('@') == 1:
        return False
    else:
        return True


@app.route("/")
def index():
    return render_template('base.html', username='', username_error='', password='', password_error='', verify_password='', verify_password_error='', email='', email_error='')

@app.route("/signup", methods=['POST'])
def validate():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    user_error_msg = ''
    pw_error_msg = ''
    verify_error_msg = ''
    email_error_msg = ''

    username_escaped = cgi.escape(username, quote=True)
    password_escaped = cgi.escape(password, quote=True)
    verify_escaped = cgi.escape(verify_password, quote=True)
    email_escaped = cgi.escape(email, quote=True)

    if username_error(username):
        user_error_msg = "Invalid Entry. Please enter a user name between 3-20 characters long, with no spaces."
        username = ''
    
    if password_error(password):
        pw_error_msg = "Invalid Entry. Please enter a password between 3 and 20 characters long, containing no spaces"
        password = ''
    
    if verify_password_error(verify_password):
        verify_error_msg = "Invalid Entry. The passwords do not match. Please try again."
        password = ''
    
    if email_error(email):
        email_error_msg = "Invalid Entry. Please enter a valid email address with no spaces."
        email = ''

@app.route('/welcome')
def valid_signup():
    if not username_error and not password_error and not verify_password_error and not email_error:
        return render_template('welcome.html', username=username)
    else:
        return render_template('base.html', username=username, username_error=user_error_msg, password_error=pw_error_msg, verify_password_error=verify_error_msg, email_error=email_error_msg)
    

app.run()