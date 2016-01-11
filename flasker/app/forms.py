#coding:utf-8
from flask.ext.wtf import Form
from wtforms import * 
from wtforms.validators import DataRequired
class lyb(Form):
	 text=TextAreaField(u'标题', validators=[DataRequired()])
	 title=StringField(u'内容', validators=[DataRequired()])
