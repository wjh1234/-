# -*- coding: UTF-8 -*-   
from flask import render_template, flash, redirect
from sqlalchemy.orm import *
from sqlalchemy import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask import *
from forms import lyb 
#from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI']='mysql://dj:123456@localhost/wjh'
#bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(300), unique=True)
    text = db.Column(db.Text)

    def __init__(self, titel,text):
                self.text = text
                self.titel=titel


db.create_all()
@app.route('/add', methods=['GET', 'POST'])
def register():
	form = lyb(request.form)
	if request.method == 'POST' and form.validate():
		user=User(form.title.data,form.text.data)
		db.session.add(user)
		db.session.commit()
		flash('Thanks for registering')
		return redirect(url_for('index'))
	return render_template('text.html', form=form)
@app.route('/index') 
def index():
	p = User.query.order_by(User.id.desc()).all()
	return render_template('index.html',p=p)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    p =User.query.get_or_404(id)
    return render_template('index.html_1.html', p=p)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
	post = User.query.get_or_404(id)
	form = lyb(request.form)
	if request.method == 'POST' and form.validate():
		post.titel=form.title.data
		post.text=form.text.data
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	form.title.data=post.titel
	form.text.data=post.text
	return render_template('text_1.html', form=form,post=post)
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	post = User.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('index'))
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
