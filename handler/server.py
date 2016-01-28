#!/usr/bin/python
#coding=utf-8

from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sqlite3
from contextlib import closing

DATABASE = '/tmp/flaskr.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db_source = {'/login': 'user.sql',
             '/add': 'entry.sql',
             '/list': 'entry.sql'}


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('entry.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/list')
def show_entries():
    cur = g.db.execute("select title, text from entries order by id desc")
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uid = request.form['username']
        pwd = request.form['password']
        sql = "select id from user where username = '%s' and password = '%s'" % (uid, pwd)
        print "sql: ", sql
        user = g.db.execute(sql)
        if user:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        g.db.execute('insert into user (username, password) values (?, ?)',
                     [request.form['username'], request.form['password']])
        g.db.commit()
        return render_template('login.html', error=error)
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/')
def hello():
    return 'hello world!'


@app.route('/sun_and_earth', methods=['GET'])
def sun_and_earth():
    print 'in'
    return render_template('sun_and_earth.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
