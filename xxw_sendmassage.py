# coding=utf-8
import sys
import  requests
import re
s=requests.Session()
import time
import itertools

sendurl="http://www.xinxianwang.com/forum/mess_send.asp"
auth_url = "http://www.xinxianwang.com/login/login.asp"
values = {
"username":"cqmyg123334",
"password":"cqmyg123",
"k":"Fri Oct 23 2015 23:39:12 GMT+0800 (中国标准时间)40000"
 }

post_header ={
 "Referer":"http://www.xinxianwang.com/login",
 "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
 "Accept-Encoding":"gzip, deflate",
 "Accept-Language":"zh-CN,zh;q=0.8",
 "Connection":"keep-alive"
    }

print s.post(auth_url,data=values).content
d=0
for i in xrange(1,229):
	frurl="http://www.xinxianwang.com/forum/user/find.asp?page=%d&username=&view=" %(i)
	#frurl="http://www.xinxianwang.com/forum/thread-9512150-1-1.html"
	print frurl
	html=s.get(frurl).content
	username=re.findall(r'index.asp\?username\=.* target',html)
	print username
	name=re.findall(r'<li><a href="/forum/user/index.asp\?username\=.* target\="_blank">.*?</a>',html)
	print name
	title=u"加入新县同城交友群".encode('gbk')
	n=0
	func = lambda x,y:x if y in x else x + [y]
	username=reduce(func, [[], ] + username)
	for smsuser,name in zip(username,name):
		smsuser=smsuser.split('username=')[1].split(" ")[0].replace("\"","")
		name=name.split('target="_blank">')[1].split('</a>')[0]
		info="%s  %s"%(name,smsuser)
		infourl="http://www.xinxianwang.com/forum/user/info.asp?username="+smsuser
		print infourl
		#f=open("xxwinfo.txt","a")
		#f.write(info+"\n")
		senddata={
		"SmsUserName":smsuser,
		"SmsTitle":title,
		"SmsMessage":u"本群是新县最大的真实、严肃的单身交友群。本群的人员主要都是优秀的，素质高、学历高的新县单身男女。入群条件：1. 必须是单身。 2. 男20岁以上，女20岁以上适婚年龄。3. 在新县或者外地有稳定的工作。 4. 相信爱情，感情专一。 5. 以结婚为前提找对象，严肃！缘来如此1号群490087869".encode("gbk"),
		"ac":"save"
		}
		print s.post(sendurl,data=senddata).content
		n=n+1
	print n




