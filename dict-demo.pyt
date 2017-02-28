
#!/usr/bin/env python


'''
  二维数据累加
  通过字典对列表的元素做索引，对符合要求的数据进行累加
‘’‘
data=[['esb',2,3],['esb',2,5],['pda',5,8]]
dic={}
for x in data:
        if x[0] not in  dic:
                dic[x[0]]=[x[1],x[2]]
        else:
                dic[x[0]][0]+=x[1]
                dic[x[0]][1]+=x[2]
print dic



#!/usr/bin/env python 
#coding:utf-8
’‘’
读取文件文件内容
对文件内容进行字符串切分
用字典的方法对需要的数据进行累加
‘’‘
import re
from functools import reduce
from operator import add
def jsontimer():
	sum=0
	with open('log/localhost_access_log.2016-10-09.log','r') as f2:
		data=f2.readlines()
		data=[x.strip() for x in data ]
	list1=[]
	for x in data:
		timer=x.split()[-1]	
		app=x.split()[7]
		app=app.split('?')[0]
		list1.append([app,timer])
	dic={}
	dic2={}
	for k,v in list1:	
		v=float(v)
		if k not in dic:
			dic[k]=v
			dic2[k]=1
		else:
			dic[k]+=v
			dic2[k]+=1

	dic1={}
	for k,v in dic.items():
		 dic1[k]= '%.2f'%v
	list2=[]
	for k,v in dic1.items():
		result=(k,dic1[k],dic2[k])
		list2.append(result)
	return  list2
if __name__ == '__main__':
	a=jsontimer()

