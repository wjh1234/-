from sqlalchemy import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask import * 
from sqlalchemy.orm import *
from forms import lyb 
app = Flask(__name__)
CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"
app.config['SECRET_KEY']='you-will-never-guess'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://dj:123456@localhost/wjh'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(80), unique=True)
    text = db.Column(db.String(120), unique=True)

    def __init__(self, titel,text):
		self.text = text
		self.titel=titel
#db.create_all()
@app.route('/add1',methods =['GET','POST'])
def texto():
	form =lyb()
	if request.method == "POST":
		if form.validate_on_submit()== True:
			q=request.form['title']
			s=request.form['text']
			return render_template('text.html', form = form)
