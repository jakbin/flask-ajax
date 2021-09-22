from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import math
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fajax.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    '''set structure of database'''
    sno = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/loaddata")
def lodadata():
    users = User.query.filter_by().all()
    return render_template('loaddata.html', users=users)

@app.route("/insertdata", methods = ['POST'])
def insertdata():
    data = request.get_json()
    # print(data)
    # print(type(data))
    name = data['name']
    city = data['city']
    user = User(name=name, city=city)
    db.session.add(user)
    db.session.commit()
    return  "1"

@app.route("/updatedata", methods = ['POST'])
def updatedata():
    data = request.get_json()
    # print(data)
    sno = data['id']
    name = data['name']
    city = data['city']
    user = User.query.filter_by(sno=sno).first()
    user.name = name
    user.city = city
    db.session.commit()
    return  "1"

@app.route("/deletedata", methods = ['POST'])
def deletedata():
    data = request.get_json()
    # print(data)
    sno = data['id']
    user = User.query.filter_by(sno=sno).first_or_404()
    current_ssession  = db.session.object_session(user)
    current_ssession.delete(user)
    current_ssession.commit()
    return  "1"

if __name__ == "__main__":
    app.run(debug=True)