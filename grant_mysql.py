#!/usr/bin/env python
#20150413
#mysql批量授权脚本。实现ssh登录机器。对多台机器多个系统自动执行mysql授权命令。
#grant mysql 
#!/usr/bin/python 
import paramiko
import sys
user="root"
dbuser=sys.argv[1]
dbname=sys.argv[2]
dbhost= sys.argv[3:]
def scm_db(ip):
                host=ip
                password='tty@ + '.'.join(host.split('.')[-2:])
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host,36000,user, password)
                dbhost= sys.argv[3:]
                for dbht in dbhost:
                        print dbht
                        cmd = 'echo "grant select on %s.*  to  %s@%s identified by \'%s\'"  |  mysql $sql_param' %(dbn
ame,dbuser,dbht,dbuser)

                        print cmd
                        stdin,stdout,stderr=ssh.exec_command(cmd)     
                        print stdout.read()
                        print stderr.read()
host=["192.168.1.2","192.168.1.3"]

for ip in host:
        print ip
        scm_db(ip)
