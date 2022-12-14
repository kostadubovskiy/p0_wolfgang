from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import redirect, request, session, url_for
from sql_func import *
from datetime import date

app = Flask(__name__)    #create Flask object

app.secret_key = 'skey'
usernames=['yee', 'ah']
passwords = ['goofy', 'ah']
global blog_num
blog_num = 0


@app.route('/')
def index():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('index.html', username=curr_usr)

@app.route('/home')
def home():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('home.html', username=curr_usr)

@app.route('/explore')
def explore():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('explore.html', username=curr_usr)

@app.route('/create')
def create():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('create.html', username=curr_usr)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session and 'password' not in session and request.method == 'POST': # and 'username' in session and 'password' in session:
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    if 'username' in session:
        # print(session)
        # print(entry_exists("usernames", ("username", session['username'])))
        if entry_exists("usernames", ("username", session['username'])):
            # print (read_entry("usernames", ("username", session['username']),"password"))
            if read_entry("usernames", ("username", session['username']),"password")[0] == session['password']:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                msg = 'Wrong password'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Wrong username'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        session['nusername'] = request.form['nusername']
        session['npassword'] = request.form['npassword']
        session['vnusername'] = request.form['vnusername']
        session['vnpassword'] = request.form['vnpassword']

    if 'nusername' in session and 'npassword' in session:
        if session['nusername'] ==  session['vnusername'] and session['npassword'] == session['vnpassword']:
            new_usr = session['nusername']
            new_pass = session['npassword']
            if not entry_exists("usernames", ("username",new_usr)):
                add_entry("usernames", (new_usr, new_pass))
            else:
                msg = "Username already taken"
                return render_template("add_account.html", msg=msg)
            session.pop('nusername', None)
            session.pop('npassword', None)
            session.pop('vnusername', None)
            session.pop('vnpassword', None)
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('login'))

        elif session['nusername'] != session['vnusername']:
            if session['npassword'] != session['vnpassword']:
                msg = "Usernames and passwords don't match"
                return render_template('add_account.html', msg=msg)
            else:
                msg = "Usernames don't match"
                return render_template('add_account.html', msg=msg)
        else:
            msg = "Passwords don't match"
            return render_template('add_account.html', msg=msg)
    return render_template('add_account.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/delete_account')
def delete_account():
    # remove the username from the session if it's there
    delete_entry("usernames", ("username", session['username'])) 
    session.pop('username', None)
    session.pop('password', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/post_blog')
def post_blog(): 
    title = request.form['title']
    body = request.form['body']
    blog_num += 1
    today = date.today()
    print(f"{title}, {body}, {blog_num}, {today}, {session['username']}")
    add_entry("blogs", (blog_num, session['username'], title, today, "blurb", body))
    print(f"{title}, {body}, {blog_num}, {today}, {session['username']}")
    session.pop('title', None)
    session.pop('body', None)
    return redirect(url_for('home'))


@app.route('/create')
def create_blogs():
    return "hi"

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
