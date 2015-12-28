# wjhtest
#爬取糗事百科的段子
#coding=utf-8
import time
import requests 
import sys
import sys 
import json
import re
import threading
from bs4 import BeautifulSoup 
import urllib2
import time
import re
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
r=requests.Session()
url="http://www.qiushibaike.com/"
html=r.get(url).content.decode('utf-8')
soup = BeautifulSoup(html)
html1=soup.findAll('div',attrs={'class' : "content"})
for html in html1:
    print html.get_text("-", strip=True) #通过get_text 方法获取标签里面的文本内容。然后strip方法是取出前后空格和空行  
