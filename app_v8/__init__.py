from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import redirect, request, session, url_for
from sql_func import *
from datetime import datetime
import random

app = Flask(__name__)    #create Flask object

app.secret_key = 'skey'


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

    my_blogs = sort_bycol("blogs",("author",curr_usr),"blog_id")
    print(my_blogs)

    if len(my_blogs) == 0:
        return render_template('home.html',text="no blogs published")
    else:
        blog_list = []
        for blog in my_blogs:
            print(blog[0])
            print(read_entry("blogs",("blog_id",blog[0]),"*"))
            blog_list.append(read_entry("blogs",("blog_id",blog[0]),"*"))
        
    
    
    return render_template('home.html',text=blog_list)

@app.route('/explore')
def explore():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('explore.html', username=curr_usr)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body']
        blurb = request.form['blog_blurb']
        today = datetime.now()
        today = today.strftime("%d/%m/%Y %H:%M:%S")
        blog_id = random.randrange(1000000000)
        while entry_exists("blogs", ("blog_id", blog_id)):
            blog_id = random.randrange(1000000000)
        add_entry("blogs", (str(blog_id), curr_usr, title, today, blurb, body))
    return render_template('create.html')




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

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
