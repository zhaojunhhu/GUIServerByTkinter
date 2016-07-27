# -*- coding: utf-8 -*-
#*		主要用于保存系统运行中产生的连接信息，分为TCP、UDP两个接口
import datetime
import os
import os.path
import json
import re
######正则表达式过滤内容
def Filter(strs,guize):    ###正则表达式过滤内容
	myItems = re.findall(guize,strs,re.S)
	Items = ''.join(myItems)
	return Items

###监听到UDP端口数据保存
def AddRecv_UdpLogs(newdat,ip):                                     #向创建的文件内添加信息
	testhandle = open('Log\log.txt','a')
	testhandle.writelines(str(datetime.datetime.now())+'UdpRecv<<<<<'+newdat+'\n\r')
	testhandle.close()
	print ip
	#SaveOnuLogs(newdat,ip)
	return '%s--RecvUdp:\n%s\n\n'%(datetime.datetime.now(),newdat)

###UDP端口发送出的数据保存
def AddSend_UdpLogs(newdat):                                     #向创建的文件内添加信息
	testhandle = open('Log\log.txt','a')
	testhandle.writelines(str(datetime.datetime.now())+'UdpSend>>>>>'+newdat+'\n\r')
	testhandle.close()
	return '%s--SendUdp:\n%s\n\n'%(datetime.datetime.now(),newdat)

###监听到TCP端口数据保存
def AddRecv_TcpLogs(newdat):                                     #向创建的文件内添加信息
	testhandle = open('Log\log.txt','a')
	testhandle.writelines(str(datetime.datetime.now())+'TcpRecv<<<<<'+newdat+'\n\r')
	testhandle.close()
	return '%s--RecvTcp:\n%s\n\n'%(datetime.datetime.now(),newdat)

###TCP端口发送出的数据保存
def AddSend_TcpLogs(newdat):                                     #向创建的文件内添加信息
	testhandle = open('Log\log.txt','a')
	testhandle.writelines(str(datetime.datetime.now())+'TcpSend>>>>>'+newdat+'\n\r')
	testhandle.close()
	return '%s--SendTcp:\n%s\n\n'%(datetime.datetime.now(),newdat)

def SaveOnuLogs(data,ip):
	path =os.getcwdu() +'\Log\OnuLog'
	ipaddr = str(ip[0])
	ipport = str(ip[1])
	ansDate = json.loads(data)
	sermac = 'FFFFFFFFFFFFFF'
	if 'MAC' in data:
		try:
			sermac=ansDate['MAC']
		except KeyError:
			sermac='FFFFFFFFFFFFFF'
	else:
		sermac='FFFFFFFFFFFFFF'
	OnuLogName = sermac+'_'+ipaddr+'-'+ipport+'_.txt'
	dir_name = os.listdir("Log\OnuLog")
	count = len(dir_name)  #返回文件的行数
	ct = 0
	if count == 0:
		try:
			f = open(path+'\\'+OnuLogName, 'a')
			f.writelines(data+'\n\r')
		except ValueError:
			print u"写入成功"
		finally:
			f.close()
	while ct < count:
		onu = dir_name[ct]
		mac = dir_name[ct][0:12]
		Ip = Filter(onu,"_(.*?).txt")
		oldIp = Filter(Ip,"(.*?)-")
		oldPort=Filter(Ip,"-(.*?)_")
		print u"查询到的日志log信息",u"MAC",mac,u"Ip",oldIp,u"Port",oldPort
		if ipport == oldPort:
				OnuLogName = path+'\\'+dir_name[ct]
				try:
					f = open(OnuLogName, 'a')
					f.writelines(data+'\n\r')
				except ValueError:
					print u"写入成功"
				finally:
					f.close()
		elif sermac in dir_name[ct]:
				newname = dir_name[ct].replace(oldPort,ipport).replace(oldIp,ipaddr)
				os.rename(os.path.join(path,dir_name[ct]), os.path.join(path,newname))
				OnuLogName = path+'\\'+newname
				try:
					f = open(OnuLogName, 'a')
					f.writelines(data+'\n\r')
				except ValueError:
					print u"写入成功"
				finally:
					f.close()
		else:
				OnuLogName =  path+'\\'+sermac+'_'+ipaddr+'-'+ipport+'_.txt'
				try:
					f = open(OnuLogName, 'a')
					f.writelines(data+'\n\r')
				except ValueError:
					print u"写入成功"
				finally:
					f.close()
		ct+=1

