# -*- coding:utf-8 -*-
import json,simplejson
import base64,os
from OnuList.Readonulist import *
from RunningOnu import *

####DiangoWeb查询设备录入信息
def WebDjangoFindOnuInfo(data):
	info = {"Result":"-1"}
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr']
		if Serche_OnuList(ansaddr) == True:
			onuinfo = ReadConfigOnuData(ansaddr)
			info["Info"] = onuinfo
			info["Result"] = "0"
			info = json.dumps(info)
			print u"当前设备已存在"
		else:
			info = json.dumps(info)
			print u"当前设备不存在"
	finally:
		return info

####DiangoWeb异常流程对接测试请求
def WebDjangoOnuRunInfo(data):
	info = {"Result":"-1"}
	info1 = {}
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr'].encode("utf-8")
		if Serche_OnuList(ansaddr) == True:				###待测试设备确认已经录入
			info1 = json.loads(data)['data']		#提取测试配置信息
			Get_WebLable_aa_list(ansaddr,info1["FenFaBootFirst"].encode("utf-8"))	#写入测试信息到系统变量中
			Get_WebLable_bb_list(ansaddr,info1["FenFaBootFirst"].encode("utf-8"))
			Get_WebLable_a_list(ansaddr,info1["YunYingBoot"].encode("utf-8"))
			Get_WebLable_b_list(ansaddr,info1["YunYingRegister"].encode("utf-8"))
			Get_WebLable_c_list(ansaddr,info1["YunYingHb"].encode("utf-8"))
			Get_WebLable_d_list(ansaddr,info1["YunYingRequestPlug"].encode("utf-8"))
			Get_WebLable_e_list(ansaddr,info1["ChaJianAA5"].encode("utf-8"))
			Get_WebLable_f_list(ansaddr,info1["ChaJianAA6"].encode("utf-8"))
			Set_RunONTMac(ansaddr)
			Set_RunONTFlag(1)								#命令标志位
			info["Result"] = "0"
		else:
			info["Result"] = "-1"		###待测试设备确认没有录入
	finally:
		info = json.dumps(info)
		return info

####DiangoWeb网关能力测试请求
def WebDjangoTestOnuInfo(data):   ####webdjango TestOnu消息中Info消息处理
	infos = {"Result":"-1"}
	info = ''
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr'].encode("utf-8")
		if Serche_OnuList(ansaddr) == True:				###待测试设备确认已经录入
			info1 = json.loads(data)['data'].encode("utf-8")  ###
			info2 = re.findall('{(.*?){(.*?)}}',info1) 	#命令内容部分，提取Parameter值并进行base64加密
			dataline5 =  "{"+info2[0][0]
			dataline6 = "{"+info2[0][1]+"}"			#Parameter值
			endataline6 = base64.b64encode(dataline6)
			info  = dataline5+"\""+endataline6+"\"}"	#重新组合
			Set_RunONTMac(ansaddr)
			Set_RunCmdType(info)
			Set_RunONTFlag(1)								#命令标志位
			infos["Result"] = "0"
		else:
			info["Result"] = "-1"		###待测试设备确认没有录入
	finally:
		#for (k,v) in GlobalVar.ONT.items():
		#	print '%s:%s' %(k, v)
		infos = json.dumps(infos)
		return infos

def WebDjangoGetTestOnuInfo(data):
	info = {"Result":"-1"}
	ansaddr = 'None'
	try:
		ansaddr = json.loads(data)['OnumacAddr']
		if Serche_OnuList(ansaddr) == True:
			if Get_RunONTMac() == ansaddr:
				info["Result"] = "0"
				info["TestInfo"] =ReadRunningOnu(ansaddr)
				info = json.dumps(info)
				print u"当前设备为待测试设备"
			else:
				info["Result"] = "1"
				info["TestInfo"] ="0"
				info = json.dumps(info)
				print u"当前设备已录入，不属于测试设备"
		else:
			info = json.dumps(info)
			print u"当前设备不存在"
	finally:
		return info

###(aa)网关向分发平台注册
def Get_WebLable_aa_list(mac,info):
	FenFaBoot = (0,0)
	print mac
	if info== "00":
		FenFaBoot = (0,0)
		print u"aa)网关向分发平台注册:[未设置]"
	elif info=="0":
		FenFaBoot=(0,0)
		print u"aa)网关向分发平台注册:[返回0, 连接成功]"
	elif info=="-1":
		FenFaBoot=(0,-1)
		print u"aa)网关向分发平台注册:[返回-1，不响应]"
	elif info=="-2":
		FenFaBoot=(0,-2)
		print u"aa)网关向分发平台注册:[返回-2，静默150分钟再重新注册]"
	Set_RunFenFaBoot(FenFaBoot)

###(bb)网关向分发平台注册2
def Get_WebLable_bb_list(mac,info):
	FenFaRegister= (0,2)
	if info=="00":
		FenFaRegister= (0,2)
		print u"bb)网关向分发平台注册（2）:[未设置]"
	elif info=="2":
		FenFaRegister=(0,2)
		print u"bb)网关向分发平台注册（2）:[返回2, 连接成功]"
	elif info=="-11":
		FenFaRegister=(1,2)
		print u"bb)网关向分发平台注册（2）:[平台没有响应，终端应用相同服务器端口重试。]"
	elif info=="-12":
		FenFaRegister=(2,2)
		print u"bb)网关向分发平台注册（2）:[运营平台响应超时，网关向分发平台发起平台注册.]"
	elif info=="-2":
		FenFaRegister=(0,-2)
		print u"bb)网关向分发平台注册（2）:[返回-2，静默150分钟重新注册]"
	Set_RunFenFaRegister(FenFaRegister)

###(a)网关向运营平台注册
def Get_WebLable_a_list(mac,info):
	YunYingBoot= (0,0)
	if info=="00":
		YunYingBoot= (0,0)
		print u"a)  网关向运营平台注册:[未设置]"
	elif info=="0":
		YunYingBoot= (0,0)
		print u"a)  网关向运营平台注册:[返回0同时返回ChallengeCode。]"
	elif info=="-1":
		YunYingBoot= (0,-1)
		print u"a)  网关向运营平台注册:[平台响应超时或返回-1。]"
	elif info=="-2":
		YunYingBoot= (0,-2)
		print u"a)  网关向运营平台注册:[返回-2时，表示网关提交信息不合法。]"
	elif info=="-5":
		YunYingBoot= (0,-5)
		print u"a)  网关向运营平台注册:[返回-5时，网关开始重新注册。]"
	Set_RunYunYingBoot(YunYingBoot)

###(b)网关向运营平台注册2
def Get_WebLable_b_list(mac,info):
	YunYingRegister = (0,2)
	if info== "00":
		YunYingRegister = (0,2)
		print u"b)  网关向运营平台注册（2);[未设置]"
	elif info== "2":
		YunYingRegister = (0,2)
		print u"b)  网关向运营平台注册（2):[返回2，UserID值是否与平台先前保存该网关的UserID相同]"
	elif info== "3":
		YunYingRegister = (0,3)
		print u"b)  网关向运营平台注册（2):[返回3，UserID不相同或不存在，网关恢复出厂设置]"
	elif info== "-1":
		YunYingRegister = (2,0)
		print u"b)  网关向运营平台注册（2):[平台响应超时，网关重新发起平台注册]"
	elif info== "-2":
		YunYingRegister = (0,-2)
		print u"b)  网关向运营平台注册（2):[返回-2时，静默150分钟，再重新进行网关向平台注册]"
	elif info== "-5":
		YunYingRegister = (0,-5)
		print u"b)  网关向运营平台注册（2):[返回-5时，网关开始重新注册。]"
	Set_RunYunYingRegister(YunYingRegister)

####(c)心跳保活
def Get_WebLable_c_list(mac,info):
	Hb = (0,35)
	if info == "00":
		Hb = (0,35)
		print u"c)  心跳保活:[未设置]"
	elif info == "0":
		Hb = (0,30)
		print u"c)  心跳保活:[返回2, 连接成功]"
	elif info == "-1":
		Hb = (1,0)
		print u"c)  心跳保活:[如果30秒内没有收到回复]"
	elif info == "-3":
		Hb = (-3,0)
		print u"c)  心跳保活:[返回-3,需要网关重新向平台注册]"
	elif info == "-5":
		Hb = (-5,0)
		print u"c)  心跳保活:[返回-5,网关重新连接其它服务器]"
	Set_RunHb(Hb)

###(d)反向触发网关到插件中心
def Get_WebLable_d_list(mac,info):
	RequestPlug = (0,1)
	if info == "00":
		RequestPlug = (0,1)
		print u"d)  反向触发网关连接到插件中心:[未设置]"
	elif info == "0":
		RequestPlug = (0,1)
		print u"d)  反向触发网关连接到插件中心:[正常流程测试]"
	elif info == "-1":
		RequestPlug = (0,-1)
		print u"d)  反向触发网关连接到插件中心:[平台返回-1，重新开始网关向平台注册]"
	Set_RunYunYingRequestPlug(RequestPlug)

###(e)反向触发网关重新注册
def Get_WebLable_e_list(mac,info):
	RequestDistri = (0,1)
	if info == "00":
		RequestDistri = (0,1)
		print u"e)  反向触发网关重新注册:[未设置]"
	elif info == "0":
		RequestDistri = (0,1)
		print u"e)  反向触发网关重新注册:[正常流程测试]"
	elif info == "-1":
		RequestDistri = (0,-1)
		print u"e)  反向触发网关重新注册:[平台返回-1，重新开始网关向平台注册]"
	Set_RunYunYingRequestDistri(RequestDistri)

###(f)反向触发网关重新注册
def Get_WebLable_f_list(mac,info):
	Disconnect = ()
	if info == "00":
		Disconnect = (0,0)
		print u"f)  触发网关和插件中心断开连接:[未设置]"
	elif info == "0":
		Disconnect = (0,0)
		print u"f)  触发网关和插件中心断开连接:[触发网关和插件中心断开连接]"
	Set_RunChaJianDisconnect(Disconnect)

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

####DiangoWeb操作命令方法判断
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
		elif ans['CmdType'] =='GetTestOnuInfo':
			return 'GetTestOnuInfo'
		else:
			return False

####DiangoWebMAC地址判断
def WebDjangoOnuAddr(data):   ####webdjango消息中Onumac地址判断
	ansaddr ='None'
	try:
		ansaddr = json.loads(data)['OnumacAddr'].encode("utf-8")
	finally:
		if len(ansaddr) == 12:
			return True
		elif len(ansaddr) != 12:
			return False

def ReadRunningOnu(mac):
	info = {'CmdFlag':"",'ONTMac':"",'CmdType':"",'FenFaBoot':"",'FenFaRegister':"",
		   'YunYingBoot':"", 'YunYingRegister':"",'Hb':"",'HbPort':"",
		   'RequestPlug-in':"",'RequestDistri':"",
		   'Disconnect':""}
	if Get_RunONTFlag() == 1:
		info["CmdFlag"] = "待测试状态"
		info["ONTMac"] = Get_RunONTMac()
		info["CmdType"] = Get_RunCmdType()
	elif Get_RunONTFlag() == 0:
		info["CmdFlag"] = "未处于测试状态"
	###aa
	if Get_RunFenFaBoot() == (0,0):
		info["FenFaBoot"] = "[未设置] || [返回0, 连接成功]"
	elif  Get_RunFenFaBoot() == (0,-1):
		info["FenFaBoot"] = "[返回-1，不响应]"
	elif  Get_RunFenFaBoot() == (0,-2):
		info["FenFaBoot"] = "[返回-2，静默150分钟再重新注册]"
	###bb
	if Get_RunFenFaRegister() == (0,2):
		info["FenFaRegister"] = "[未设置] || [返回2, 连接成功]"
	elif Get_RunFenFaRegister() == (1,2):
		info["FenFaRegister"] = "[平台没有响应，终端应用相同服务器端口重试。]"
	elif Get_RunFenFaRegister() == (2,2):
		info["FenFaRegister"] = "[运营平台响应超时，网关向分发平台发起平台注册.]"
	elif Get_RunFenFaRegister() == (0,-2):
		info["FenFaRegister"] = "[返回-2，静默150分钟重新注册]"
	###a
	if Get_RunYunYingBoot() == (0,0):
		info["YunYingBoot"] = "[未设置] || [返回0同时返回ChallengeCode。]"
	elif Get_RunYunYingBoot() == (0,-1):
		info["YunYingBoot"] = "[平台响应超时或返回-1。]"
	elif Get_RunYunYingBoot() == (0,-2):
		info["YunYingBoot"] = "[返回-2时，表示网关提交信息不合法。]"
	elif Get_RunYunYingBoot() == (0,-5):
		info["YunYingBoot"] = "[返回-5时，网关开始重新注册。]"
	###b
	if Get_RunYunYingRegister() == (0,2):
		info["YunYingRegister"] = "[未设置] || [返回2，UserID值是否与平台先前保存该网关的UserID相同]"
	elif Get_RunYunYingRegister() == (0,3):
		info["YunYingRegister"] = "[返回3，UserID不相同或不存在，网关恢复出厂设置]"
	elif Get_RunYunYingRegister() == (2,0):
		info["YunYingRegister"] = "[平台响应超时，网关重新发起平台注册]"
	elif Get_RunYunYingRegister() == (0,-2):
		info["YunYingRegister"] = "[返回-2时，静默150分钟，再重新进行网关向平台注册]"
	elif Get_RunYunYingRegister() == (0,-5):
		info["YunYingRegister"] = "[返回-5时，网关开始重新注册。]"
	###c
	if Get_RunHb() == (0,35):
		info["Hb"] =  "[未设置]"
	elif  Get_RunHb() == (0,30) :
		info["Hb"] =  "[返回2, 连接成功]"
	elif  Get_RunHb() == (1,0) :
		info["Hb"] =  "[如果30秒内没有收到回复]"
	elif  Get_RunHb() == (-3,0) :
		info["Hb"] =  "[返回-3,需要网关重新向平台注册]"
	elif  Get_RunHb() == (-5,0) :
		info["Hb"] =  "[返回-5,网关重新连接其它服务器]"
	###d
	if Get_RunYunYingRequestPlug() == (0,1):
		info["RequestPlug-in"] = "[未设置] || [正常流程测试]"
	elif Get_RunYunYingRequestPlug() == (0,-1):
		info["RequestPlug-in"] = "[平台返回-1，重新开始网关向平台注册]"
	###e
	if Get_RunYunYingRequestDistri() == (0,1):
		info["RequestDistri"] = "[未设置] || [正常流程测试]"
	elif  Get_RunYunYingRequestDistri() == (0,-1):
		info["RequestDistri"] = "[平台返回-1，重新开始网关向平台注册]"
	###f
	if Get_RunChaJianDisconnect() == (0,0):
		info["Disconnect"] = "[未设置]"

	return info

