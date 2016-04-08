#!/usr/bin/env python
'''统计一个文件单词出现的个数'''
import re
with open('001.txt',"r") as f:
    data = f.read()

words = re.compile(r'([a-zA-Z]+)')
dic= {}
for x in words.findall(data):
    if x not in dic:
        dic[x] = 1
    else:
        dic[x] += 1
l=[]
for k,v in dic.items():
        l.append([k,v])
print l
for l in l:
        print l[0],l[1]
