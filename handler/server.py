#!/usr/bin/python
#coding=utf-8

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world!'


@app.route('/sun_and_earth', methods=['GET'])
def sun_and_earth():
    print 'in'
    return render_template('sun_and_earth.html')


if __name__ == '__main__':
    app.run(debug=True)
