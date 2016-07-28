# -*- coding:utf-8 -*-
import json,simplejson
import base64,os
from OnuList.Readonulist import *
from RunningOnu import *

###查询设备是否存在onulist。ini中
def Serche_OnuList(file_str):
	file_str = file_str + '.ini'###查找文件名
	dir_name = os.listdir("OnuList\List")
	count = len(dir_name)
	for i in range(0,count):
		if file_str == dir_name[i]:
			return True #设备已经被录入
		else:
			continue

###返回读取的List中指定ONU信息，入口ONU文件名
def ReadConfigOnuData(OnuMac):
	s = linecache.getline("OnuList\List\\"+OnuMac+".ini",1)
	linecache.clearcache() #很关键的一句，否则listbox调用时会刷新
	s = Filter(s,"--=(.*?)\n")
	return s

def WebMethod(data):   ####webdjango操作方法判断
	ans ={'CmdType':'None'}
	try:
		ans = json.loads(data)
	finally:
		if ans['CmdType'] == 'AddOnu':
			return 'AddOnu'
		elif ans['CmdType'] =='OnuRun':
			return 'OnuRun'
		elif ans['CmdType'] =='TestOnu':
			return 'TestOnu'
		elif ans['CmdType'] =='FindOnu':
			return 'FindOnu'
		else:
			return False

def WebDjangoFindOnuInfo(data):
	info = 'None'
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr']
		if Serche_OnuList(ansaddr) == True:
			onuinfo = ReadConfigOnuData(ansaddr)
			info = onuinfo
			print u"当前设备已存在"
		else:
			info = '2001NOK'
			print u"当前设备不存在"
	finally:
		return info

def WebDjangoOnuAddr(data):   ####webdjango消息中Onumac地址判断
	ansaddr ='None'
	try:
		ansaddr = json.loads(data)['OnumacAddr'].encode("utf-8")
	finally:
		if len(ansaddr) == 12:
			return True
		elif len(ansaddr) != 12:
			return False

def WebDjangoOnuRunInfo(data):
	info1 = {}
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr'].encode("utf-8")
		info1 = json.loads(data)['data']
		print "mac:",ansaddr
		print "FenFaBootFirst",info1["FenFaBootFirst"].encode("utf-8"),type(info1["FenFaBootFirst"].encode("utf-8"))
		print "data",info1
	finally:
		Get_WebLable_aa_list(ansaddr,info1["FenFaBootFirst"].encode("utf-8"))
		Get_WebLable_bb_list(ansaddr,info1["FenFaBootFirst"].encode("utf-8"))
		Set_RunONTMac(ansaddr)
		Set_RunONTFlag(1)								#命令标志位
		print u"写入测试设备信息成功"
		for (k,v) in GlobalVar.ONT.items():
			print '%s:%s' %(k, v)
		return '1001OK'

def WebDjangoTestOnuInfo(data):   ####webdjango TestOnu消息中Info消息处理
	info = 'None'
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr'].encode("utf-8")
		info1 = json.loads(data)['data'].encode("utf-8")  ###
		info2 = re.findall('{(.*?){(.*?)}}',info1) 	#命令内容部分，提取Parameter值并进行base64加密
		dataline5 =  "{"+info2[0][0]
		dataline6 = "{"+info2[0][1]+"}"			#Parameter值
		endataline6 = base64.b64encode(dataline6)
		info  = dataline5+"\""+endataline6+"\"}"	#重新组合
		print info
	finally:
		Set_RunONTMac(ansaddr)
		Set_RunCmdType(info)
		Set_RunONTFlag(1)								#命令标志位
		print u"写入测试设备信息成功"
		for (k,v) in GlobalVar.ONT.items():
			print '%s:%s' %(k, v)
		return '1001OK'

###(aa)网关向分发平台注册
def Get_WebLable_aa_list(mac,info):
	FenFaBoot = (0,0)
	print mac
	if info== "00":
		FenFaBoot = (0,0)
		print u"未设置"
	elif info=="0":
		FenFaBoot=(0,0)
		print u"返回0, 连接成功"
	elif info=="-1":
		FenFaBoot=(0,-1)
		print u"返回-1，不响应"
	elif info=="-2":
		FenFaBoot=(0,-2)
		print u"返回-2，静默150分钟再重新注册"
	Set_RunFenFaBoot(FenFaBoot)
	print u"FenFaBoot写入成功：",Get_RunFenFaBoot()

###(bb)网关向分发平台注册2
def Get_WebLable_bb_list(mac,info):
	FenFaRegister= (0,2)
	print mac
	if info=="00":
		FenFaRegister= (0,2)
		print u"未设置"
	elif info=="2":
		FenFaRegister=(0,2)
		print u"返回2, 连接成功"
	elif info=="-11":
		FenFaRegister=(1,2)
		print u"平台没有响应，终端应用相同服务器端口重试。"
	elif info=="-12":
		FenFaRegister=(2,2)
		print u"运营平台响应超时，网关向分发平台发起平台注册."
	elif info=="-2":
		FenFaRegister=(0,-2)
		print u"返回-2，静默150分钟重新注册"
	Set_RunFenFaRegister(FenFaRegister)
	print u"FenFaRegister写入成功：",Get_RunFenFaRegister()

###(a)网关向运营平台注册
def Get_WebLable_a_list(mac,info):
	YunYingBoot= (0,0)
	print mac
	if info=="00":
		YunYingBoot= (0,0)
		print u"未设置"
	elif info=="0":
		YunYingBoot= (0,0)
		print u"返回0同时返回ChallengeCode。"
	elif info=="-1":
		YunYingBoot= (0,-1)
		print u"平台响应超时或返回-1。"
	elif info=="-2":
		YunYingBoot= (0,-2)
		print u"返回-2时，表示网关提交信息不合法。"
	elif info=="-5":
		YunYingBoot= (0,-5)
		print u"返回-5时，网关开始重新注册。"
	Set_RunYunYingBoot(YunYingBoot)
	print u"YunYingBoot写入成功：",Get_RunYunYingBoot()

###(b)网关向运营平台注册2
def Get_WebLable_b_list(mac,info):
	YunYingRegister = (0,2)
	print mac
	if info== "00":
		YunYingRegister = (0,2)
		print u"未设置"
	elif info== "2":
		YunYingRegister = (0,2)
		print u"返回2，UserID值是否与平台先前保存该网关的UserID相同"
	elif info== "3":
		YunYingRegister = (0,3)
		print u"返回3，UserID不相同或不存在，网关恢复出厂设置"
	elif info== "-1":
		YunYingRegister = (2,0)
		print u"平台响应超时，网关重新发起平台注册"
	elif info== "-2":
		YunYingRegister = (0,-2)
		print u"返回-2时，静默150分钟，再重新进行网关向平台注册"
	elif info== "-5":
		YunYingRegister = (0,-5)
		print u"返回-5时，网关开始重新注册。"
	Set_RunYunYingRegister(YunYingRegister)
	print u"YunYingRegister：",Get_RunYunYingRegister()

####(c)心跳保活
def Get_WebLable_c_list(mac,info):
	Hb = (0,35)
	print mac
	if info == "00":
		Hb = (0,35)
		print u"未设置"
	elif info == "0":
		Hb = (0,30)
		print u"返回2, 连接成功"
	elif info == "-1":
		Hb = (1,0)
		print u"如果30秒内没有收到回复"
	elif info == "-3":
		Hb = (-3,0)
		print u"返回-3,需要网关重新向平台注册"
	elif info == "-5":
		Hb = (-5,0)
		print u"返回-5,网关重新连接其它服务器"
	Set_RunHb(Hb)
	print u"Hb：",Get_RunHb()

###(d)反向触发网关到插件中心
def Get_WebLable_d_list(mac,info):
	RequestPlug = (0,1)
	print mac
	if info == "00":
		RequestPlug = (0,1)
		print u"未设置"
	elif info == "0":
		RequestPlug = (0,1)
		print u"正常流程测试"
	elif info == "-1":
		RequestPlug = (0,-1)
		print u"平台返回-1，重新开始网关向平台注册"
	Set_RunYunYingRequestPlug(RequestPlug)
	print u"RequestPlug:",Get_RunYunYingRequestPlug()

###(e)反向触发网关重新注册
def Get_WebLable_e_list(mac,info):
	RequestDistri = (0,0)
	print mac
	if info == "00":
		RequestDistri = (0,0)
		print u"未设置"
	elif info == "0":
		RequestDistri = (0,0)
		print u"正常流程测试"
	elif info == "-1":
		RequestDistri = (0,-1)
		print u"平台返回-1，重新开始网关向平台注册"
	Set_RunYunYingRequestDistri(RequestDistri)
	print u"RunChaJianRegister: ",Get_RunYunYingRequestDistri()

###(f)反向触发网关重新注册
def Get_WebLable_f_list(mac,info):
	Disconnect = ()
	print mac
	if info == "00":
		print u"未设置"
	elif info == u"触发网关和插件中心断开连接！":
		Disconnect = (0,0)
		print u"触发网关和插件中心断开连接"
	Set_RunChaJianDisconnect(Disconnect)
	print u"Disconnect",Get_RunChaJianDisconnect()