# -*- coding:utf-8 -*-
import json

from OnuList.Readonulist import *
from RunningOnu import *

###设备BOOTFirst用，使用设备mac确认设备是否存在list文件中
def MCSEOnuMac(onumac):     	###onumac
	ans = json.loads(onumac)
	try:
		sermac=ans['MAC']
	except KeyError:
		print u"设备不存在"
		return False
	finally:
		if Serche_OnuList(sermac)== None:
			print u"设备不存在"
			return False
		elif  Serche_OnuList(sermac)== True:
			print u"设备存在"
			return True

###确认设备是否为测试设备
def MCSEOnuTestting(onumac):
	if 	 '"Result"' in onumac:
		return False
	else :
		ans = json.loads(onumac)
		try:
			sermac=ans['MAC']
		except KeyError:
			return False
		finally:
			RunningMAC = Get_RunONTMac()
			if sermac == RunningMAC:
				print u"查询到设备为当前测试设备",RunningMAC
				return True
			else:
				return False

###确认设备测试状态Flag
def MCSEOnuFlag(Flag):
	Flag = Get_RunONTFlag()
	if Flag == 1:
		print u"查询到设备为测试状态标志，Flag=",Flag
		return True
	elif Flag == 0:
		print u"查询到设备不再测试，Flag=",Flag
		return False
	else:
		return False

###判断消息为网关向分发平台发送BootFirst
def RPCMethod_BootFirst(Boot):   ####分发BootFirst
	ans = json.loads(Boot)
	if ans['RPCMethod']=='BootFirst':
		return 'BootFirst'
	else:
		return False

###判断消息为网关向分发平台发送RegisterFirst
def RPCMethod_RegisterFirst(Register):   ####分发RegisterFirst
	ans = json.loads(Register)
	if ans['RPCMethod']=='RegisterFirst':
		return 'RegisterFirst'
	else:
		return False

###判断消息为网关向运营发送Boot
def RPCMethod_Boot(Boot):   ####运营Boot
	if 	'Boot' in Boot:
		ans = json.loads(Boot)
		if ans['RPCMethod']=='Boot':
			return 'Boot'
		else:
			return False
	else :
		return False

###判断消息为网关向运营发送Register
def RPCMethod_Register(Register):   ####运营Register
	if 	'Register' in Register:
		ans = json.loads(Register)
		if ans['RPCMethod']=='Register':
			return 'Register'
		else:
			return False
	else :
		return False

###判断消息为网关向运营发送Hb
def RPCMethod_Hb(Hb):   ####运营Hb
	if 'Hb' in Hb:
		ans = json.loads(Hb)
		if ans['RPCMethod']=='Hb':
			if ans['FLAG']== '1':
				return 'Hb_FLAG1'
			elif ans['FLAG']== '0':
				return 'Hb_FLAG0'
		else:
			return False
	else:
		return False

###判断消息运营平台反向触发网关至插件中心
def RPCMethod_Hb1(Result):   ####运营Hb
	if 'Result'in Result:
		ans = json.loads(Result)
		if ans['Result']==0:
			return 'Result0'
		else:
			return False
	else:
		return False

###判断消息为网关向插件中心发送boot
def RPCMethod_ChaJianBoot(Boot):   ####运营Hb
	if 'Boot' in Boot:
		ans = json.loads(Boot)
		if ans['RPCMethod']=='Boot':
			return 'Boot'
		else:
			return False
	else :
		return False

###判断消息为网关向运营发送Register
def RPCMethod_ChaJianRegister(Register):   ####运营Register
	if 	'Register' in Register:
		ans = json.loads(Register)
		if ans['RPCMethod']=='Register':
			return 'Register'
		else:
			return False
	else :
		return False

###判断消息为网关向运营发送Heartbeat心跳包
def RPCMethod_ChaJianHeartbeat(Heartbeat):   ####运营Register
	if 	'Heartbeat' in Heartbeat:
		ans = json.loads(Heartbeat)
		if ans['RPCMethod']=='Heartbeat':
			return 'Heartbeat'
		else:
			return False
	else :
		return False

###判断消息为网关向运营发送"return_Parameter"心跳包
def RPCMethod_ChaJianParameter(Parameter):   ####运营Register
	if 	'return_Parameter' in Parameter:
		return 'return_Parameter'
	else :
		return False



