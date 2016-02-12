#!/usr/bin/python
#coding=utf-8

from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE = '/tmp/flaskr.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def _create_engine(user, password, host, port, db, autocommit=False, pool_recycle=60):
    engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=utf8&use_unicode=1' % (
        user, password,
        host, port,
        db),
        pool_size=10,
        max_overflow=-1,
        pool_recycle=pool_recycle,
        connect_args={'connect_timeout': 1, 'autocommit': 1 if autocommit else 0})
    return engine

engine = _create_engine("guevara", "Ding753951ss", "rdsgggx8ppf0310n79lst.mysql.rds.aliyuncs.com", 3306, 'guevara')


def _query(engine, sql):
    connection = engine.connect()
    result = connection.execute(sql)
    connection.close()
    return result

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


@app.route('/list')
def show_entries():
    from handler.common.entry import Entry
    rows = db_session.query(Entry).all()
    entries = [dict(title=row.title, text=row.text) for row in rows]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    from handler.common.entry import Entry
    entry = Entry(title=request.form['title'], text=request.form['text'])
    db_session.add(entry)
    db_session.commit()
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
        results = _query(engine, sql)
        user = results.fetchall()
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
        from handler.common.entry import User
        user = User(username=request.form['username'], password=request.form['password'])
        db_session.add(user)
        db_session.commit()
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
