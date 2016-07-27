# -*- coding:utf-8 -*-
import os
import json

def AddOnu(NewONUMode,NewONUMAC,NewONUSSID,NewONUSSIDPwd,NewONUUserPwd,NewONUSN):
	if len(NewONUMAC)!=12 & len(NewONUSSID)!=13 &len(NewONUSN) !=24:
		return "datafailed"
	else:
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
		return "datasucces"

def RemoveOnu(OnuMac):
	path =os.getcwdu()
	onupath = path+'\OnuList\List\\'+OnuMac+'.ini'
	os.remove(onupath)
