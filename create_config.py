#!/usr/local/easyops/python/bin/python

# -*- coding: utf-8 -*-
import requests
import logging
import base64
import sys
import json
FORMAT = '%(message)s'
# logging.basicConfig(format=FORMAT)
logger = logging.getLogger('mylog')
formatter = logging.Formatter(FORMAT)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


ORG = 1021
CMDB_HOST = '10.230.20.181'
DEPLOY_HOST = '10.253.1.115'
cmdb_header = 'cmdb.easyops-only.com'
deploy_header = 'deploy.easyops-only.com'
headers = {
    'org': ORG,
    'user': 'deppon',
    'Host': '',
}
##创建程序包
def create_package(package):
    headers['Host'] = deploy_header
    url = 'http://%s/package' % CMDB_HOST
    a,b,c,d=0,1,2,3	
    ##程序包
    for  i in package:
	if i[c]=='6'and 'common' in i[d]:
		installPath='/opt/%s' %(i[d])
	elif i[c]=='5' and  'common' in i[d]:
		installPath='/opt/%s' %(i[d])
	elif i[c] == '6':
		installPath='/opt/apps/%s/deployments' %(i[d])
	else:
		installPath='/opt/apps/%s/deploy' %(i[d])
    	data={
		 'name':i[d],
	 	'type':1,
	 	'cId':1,
	 	'memo':'test',
	 	'installPath':installPath,
		}
    	data1={
		'name':'%s-%s环境' %(i[d],i[0]),
	 	'type':2,
	 	'cId':1,
	 	'memo':'test',
	 	'installPath':installPath,
		}
    	resp = requests.post(url, data=data, headers=headers)
    	resp1 = requests.post(url, data=data1, headers=headers)
    	code=resp.json()['code']
    	code1=resp.json()['code']
        if code == 100307 or code == 10037:
		print  '%s程序包/配置包已创建' %(i[d])
		continue
	else:
		print resp1.json()
		print resp1.json()
		logger.info('%s 程序包已创建过了' %(i[d]))
class create_cluster(object):
	def __init__(self):
		self.CMDB_HOST = '10.230.20.181'
		self.ORG=1021
		self.DEPLOY_HOST = '10.253.1.115'
		self.cmdb_header = 'cmdb.easyops-only.com'
		self.deploy_header = 'deploy.easyops-only.com'
		self.headers = {'ORG':self.ORG,'user':'easyops','host':''}
	##获取机器的实例value
	def get_instance(self,*ip):
		ip=ip[5::]
		url= 'http://%s/object/instance/list/HOST' % self.CMDB_HOST
		params = {'page': 1,'pageSize': 200}
		headers['Host'] = cmdb_header
		ip_info=[]
		if ip:
			for ip1 in ip:
				params['ip$eq']= base64.b64encode(ip1)
				try:
					resp = requests.get(url, params=params, headers=headers)
					recs = resp.json()['data'].get('list', [])
					result1=recs[0]['instanceId']
					ip_info.append(result1)
				except:	
					logger.error('%s is not exist' %(ip1))
			#ip_info=';'.join(ip_info)
			return ip_info 
	def get_app_name(self,app_name):
		url = 'http://%s/object/instance/list/APP' % self.CMDB_HOST
    		params = {
        		'page': 1,
       		 	'pageSize': 200,
    		}
    		if app_name:
        		params['name$eq'] = base64.b64encode(app_name), 
    		headers['Host'] = self.cmdb_header

    		resp = requests.get(url, params=params, headers=headers)

    		apps = []
    		recs = resp.json()['data'].get('list', [])

    		for rec in recs:
			try:
        			apps.append({
            				'name': rec['name'],
            				'appId': rec['appId'],
            				'_packageList': rec.get('_packageList', []),
            				'clusters': rec['clusters'],
            				'status': 0,
        				})
			
			except:
				apps.append({
                                        'name': rec['name'],
                                        'appId': rec['appId'],
            				'status': 1,
                                       # '_packageList': rec.get('_packageList', []),
                                       # 'clusters': rec['clusters'],
                                        })
	

    		return  apps
	

	


		

def read_file(path):
	with  open(path, 'r') as f1:
        	line = [item.strip() for item in f1.readlines()]
		#程序包列表
		app_info=[]
            	for lines  in line:
                	if not lines:
                            continue
			#程序包
                	apps=lines.split(' ')[0].split(',')
			app_info.append(apps)
		return app_info

def main():
	package=read_file('config_list')
        create_package(package)
	t=create_cluster()
	for i in package:
		app_name=i[3]
		cluster_name=i[4]
		ip_list=t.get_instance(*i)
		appinfo2=t.get_app_name(app_name)
		if not appinfo2:
			logger.error( 'null')
			continue
		status=appinfo2[0]['status']
		###如果状态值等于0，就要进行集群校验
		if status == 0:
			try:
				for cluster in  appinfo2[0]['clusters']:
					if cluster_name.decode('utf-8')  ==    cluster['name']:
						raise 'cluster wrong'
			except:
				 logger.error('%s 集群重复' %(cluster_name))
				 continue
		url='http://%s/cluster' %(CMDB_HOST)
                data={
                                        'appId':appinfo2[0]['appId'],
                                        'name':cluster_name,
                                        'type':i[5],
                                        'deviceList':ip_list}

                resp = requests.post(url, json=data, headers=headers)
                print resp.json()
                print app_name,cluster_name,resp.text
		
        #create_package(package)
		

if __name__ == '__main__':
	main()
