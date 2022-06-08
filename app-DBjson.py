from flask import Flask, render_template, request, json, Response
from dbjson import DBjson

app = Flask(__name__)
app.secret_key = 'super-secret-key'

db = DBjson('sqlite:///fajax.db')

class User(db.Model):
    '''set structure of database'''
    sno = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)

@app.route("/")
def home():
    return render_template('index-DBjson.html')

@app.route("/loaddata")
def lodadata():
    data = db.getall(User)
    return custom_response(data, 200)

def custom_response(res, status_code):
    return Response(mimetype="application/json",response=json.dumps(res),status=status_code)

@app.route("/insertdata", methods = ['POST'])
def insertdata():
    add_data = request.get_json()
    db.add(User, add_data)
    return  "1"

@app.route("/updatedata", methods = ['POST'])
def updatedata():
    update_data = request.get_json()
    db.update(User, update_data, 'sno')
    return  "1"

@app.route("/deletedata", methods = ['POST'])
def deletedata():
    delete_data = request.get_json()
    db.delete(User, delete_data)
    return  "1"

if __name__ == "__main__":
    app.run(debug=True)
    