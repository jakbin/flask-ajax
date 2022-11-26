from flask import Flask, render_template, request, json, Response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
import math

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

class UserSchema(Schema):
  sno = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  city = fields.Str(required=True)

user_schema = UserSchema()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/loaddata", methods = ['POST'])
def lodadata():
    data = request.get_json()
    page_num = data['page_num']
    users = User.query.filter_by().all()
    total_pages = math.ceil(len(users)/5)
    users_data = users[(int(page_num)-1)*int(5): (int(page_num)-1)*int(5)+ int(5)]
    users_data = user_schema.dump(users_data, many=True)
    data = {"users": users_data, "total_pages": total_pages, "page_num":page_num}
    return custom_response(data, 200)

def custom_response(res, status_code):
    return Response(mimetype="application/json",response=json.dumps(res),status=status_code)

@app.route("/insertdata", methods = ['POST'])
def insertdata():
    data = request.get_json()
    name = data['name']
    city = data['city']
    user = User(name=name, city=city)
    db.session.add(user)
    db.session.commit()
    return  "1"

@app.route("/updatedata", methods = ['POST'])
def updatedata():
    data = request.get_json()
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
    sno = data['id']
    user = User.query.filter_by(sno=sno).first_or_404()
    current_ssession  = db.session.object_session(user)
    current_ssession.delete(user)
    current_ssession.commit()
    return  "1"

@app.route("/searchdata")
def searchdata():
    search_query = request.args.get('q')
    search = "%{0}%".format(search_query)
    dataName =  User.query.filter(User.name.like(search))
    dataCity =  User.query.filter(User.city.like(search))
    data = dataName.union(dataCity).all()
    if data == []:
        return "0"
    else:
        r_data = user_schema.dump(data,many=True)
        return custom_response(r_data, 200) 

if __name__ == "__main__":
    app.run(debug=True)
    