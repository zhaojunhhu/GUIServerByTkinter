# -*- coding:utf-8 -*-
import os
import json
from Readonulist import *

###DiangoWeb新增测试设备请求
def AddOnu(NewONUMode,NewONUMAC,NewONUSSID,NewONUSSIDPwd,NewONUUserPwd,NewONUSN):
	info = {"Result":"-1"}
	if (len(NewONUMAC)!=12) | (len(NewONUSSID)!=13) | (len(NewONUSN) !=24):	#判断设备信息是否合法。不合法返回-2
		info["Result"] ="-2"
		info = json.dumps(info)
		return info
	else:
		if Serche_OnuList(NewONUMAC) ==True:#判断设备是否已经存在，已存在返回"1"。并默认允许修改设备信息
			info["Result"] ="1"
		else:
			info["Result"] ="0" #设备新增、修改标志为”0“
		path =os.getcwdu()
		Demo = '{"SSID": "", "SSID-Pwd": "","MAC": "", "SN": "", "user-Pwd": "",  "Mode": ""}'
		OnuDemo = json.loads(Demo)
		OnuDemo['Mode'] = NewONUMode
		OnuDemo['MAC'] = NewONUMAC
		OnuDemo['SSID'] = NewONUSSID
		OnuDemo['SSID-Pwd'] = NewONUSSIDPwd
		OnuDemo['user-Pwd'] = NewONUUserPwd
		OnuDemo['SN'] = NewONUSN
		OnuDemo = '----='+json.dumps(OnuDemo)
		f = open(path+'\OnuList\List\\'+NewONUMAC+'.ini',"w+")
		f.write(OnuDemo)
		f.close()
		info = json.dumps(info)
		return info

def RemoveOnu(OnuMac):
	path =os.getcwdu()
	onupath = path+'\OnuList\List\\'+OnuMac+'.ini'
	os.remove(onupath)
