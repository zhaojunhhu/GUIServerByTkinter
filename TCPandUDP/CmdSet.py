# -*- coding:utf-8 -*-
import json
import random
from ServerSettings.ReadServerSettings import *
import hashlib

###产生32位随机数，返回str型
def ChallengeCode():
	list = 0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','A','B','C','D','E','F'
	slice = random.sample(list, 32)  # 从list中随机获取5个元素，作为一个片断返回
	CODE=str(slice).replace(",","").replace("'","").replace(" ","").replace("[","").replace("]","")
	return CODE

####生成-分发平台BootFirst消息,入口result，返回str型消息
def SendBootFirst(Result):
	str = ChallengeCode()  #获取随机32字符
	data = {"Result":Result}#list对象
	data["ChallengeCode"]=str #添加Challengecode
	data_string = json.dumps(data)  #转为json格
	#print type(data_string)
	return data_string

####生成-分发平台RegisterFirst消息,入口result，返回str型消息
def SendRegisterFirst(Interval,Result):
	data = {"Interval":Interval,"Result":Result,"ServerAddr":"","ServerPort":1}#list对象
	data["ServerAddr"]=ReadSettingsLineName(1) #添加运营服务器地址（主机地址）
	data["ServerPort"]=int(ReadSettingsLineName(3))#添加运营服务器UDP Port（60001）
	data_string = json.dumps(data)  #转为json格
	return data_string

###生成-运营平台Boot消息，入口Result,Interval,flag，返回str型消息
def SendBoot(Result,Interval,flag):
	str = ChallengeCode()  #获取随机32字符
	data = {"Result":Result,"ChallengeCode":"","Interval":Interval,"flag":""}#list对象
	data["ChallengeCode"]=str #添加Challengecode
	data["flag"]=flag
	data_string = json.dumps(data)  #转为json格
	#print type(data_string)
	return data_string

###生成-运营平台Register消息，入口Result返回str型消息
def SendRegister(Result):
	data = {"Result":Result,"UPDATEServer":"","MessageServer":""}#list对象
	data["UPDATEServer"]=ReadSettingsLineName(1) #添加运营服务器地址（主机地址）
	#添加运营服务器+UDP Port（61.165.242.141:60002）
	data["MessageServer"]=ReadSettingsLineName(1)+':'+ReadSettingsLineName(3)
	data_string = json.dumps(data)  #转为json格
	return data_string

###生成心跳消息
def SendHb(Result,Interval):
	data = {"Result":Result,"Interval":Interval}#list对象
	data_string = json.dumps(data)  #转为json格
	return data_string
###反向触发相应消息
def SendHb1(Result):
	data = {"Result":Result}#list对象
	data_string = json.dumps(data)  #转为json格
	return data_string
###生成反向触发插件中心消息
def SendRequestPlug(recv):
	recv = json.loads(recv)
	onumac=recv['MAC']
	OnuData = linecache.getline("OnuList\List\\"+onumac+".ini",1)
	linecache.clearcache() #很关键的一句，否则listbox调用时会刷新
	OnuData = Filter(OnuData,"--=(.*?)\n")
	NewData = json.loads(OnuData)
	DevRND = NewData['DevRND']
	SN = NewData['SN']
	SSIDName = NewData['SSID'][9:]
	SSIDPwd = NewData['SSID-Pwd']
	USERPwd = NewData['user-Pwd']
	sourceKEY = DevRND+SN+SSIDName+SSIDPwd+USERPwd
	myMd5 = hashlib.md5()
	myMd5.update(sourceKEY)
	KEY = myMd5.hexdigest().upper()
	data = {"RPCMethod":"RequestPlug-in","Key":"","ServerAddr":"","ServerPort":""}
	data["ServerAddr"] = ReadSettingsLineName(1) #添加插件服务器地址（主机地址）
	data["ServerPort"] = ReadSettingsLineName(4)#插件端口  tcp 60002
	data["Key"] = KEY
	data_string = json.dumps(data)  #转为json格
	return data_string

###生成反向触发网关重新注册RequestDistri
def SendRequestDistri(recv,mode):
	recv = json.loads(recv)
	onumac=recv['MAC']
	OnuData = linecache.getline("OnuList\List\\"+onumac+".ini",1)
	linecache.clearcache() #很关键的一句，否则listbox调用时会刷新
	OnuData = Filter(OnuData,"--=(.*?)\n")
	NewData = json.loads(OnuData)
	DevRND = NewData['DevRND']
	SN = NewData['SN']
	SSIDName = NewData['SSID'][9:]
	SSIDPwd = NewData['SSID-Pwd']
	USERPwd = NewData['user-Pwd']
	sourceKEY = DevRND+SN+SSIDName+SSIDPwd+USERPwd
	myMd5 = hashlib.md5()
	myMd5.update(sourceKEY)
	KEY = myMd5.hexdigest().upper()
	data = {"RPCMethod":"RequestDistri","Key":"","ServerAddr":"","ServerPort":"","mode":""}
	data["ServerAddr"] = ReadSettingsLineName(1) #添加插件服务器地址（主机地址）
	data["ServerPort"] = ReadSettingsLineName(4)#插件端口  tcp 60002
	data["Key"] = KEY
	data["mode"] = mode
	data_string = json.dumps(data)  #转为json格
	return data_string

###生成插件中心平台Boot消息，入口Result,Interval,flag，返回str型消息
def SendChaJianBoot(Result):
	str = ChallengeCode()  #获取随机32字符
	data = {"Result":Result,"ChallengeCode":""}#list对象
	data["ChallengeCode"]=str #添加Challengecode
	data_string = json.dumps(data)  #转为json格
	return data_string
###生成插件中心平台Register消息，入口Result返回str型消息
def SendChaJianRegister(Result):
	data = {"Result":Result}#list对象
	data_string = json.dumps(data)  #转为json格
	return data_string
###生成插件中心平台Register消息，入口Result返回str型消息
def SendChaJianHeartbeat(Result):
	data = {"Result":Result}#list对象
	data_string = json.dumps(data)  #转为json格
	return data_string
###生成插件中心平台Register消息，入口Result返回str型消息
def SendChaJianParameter(Parameter):
	data = {"Result":Parameter}#list对象
	data_string = json.dumps(data)  #转为json格
	return data_string

def TCP_Send(Cmd):
	strlen=len(Cmd)   #计算数据长度
	i=strlen/256
	j=strlen%256
	DatHeard = chr(0)+chr(0)+chr(i)+chr(j)  #添加长度
	NewCmd = DatHeard+Cmd
	return NewCmd