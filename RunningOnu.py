# -*- coding:utf-8 -*-
class GlobalVar:
	ONT = {'CmdFlag':0,'ONTMac':"112233445566",'CmdType':"TestCmdType",
		   'FenFaBoot':(0,0),'FenFaRegister':(0,2),
		   'YunYingBoot':(0,0), 'YunYingRegister':(0,2),'Hb':(0,35),'HbPort':(0),
		   'RequestPlug-in':(0,1),'RequestDistri':(0,1),
		   'Disconnect':(0,0)
		   }
def Set_RunONTFlag(CmdFlag):
	GlobalVar.ONT['CmdFlag'] = CmdFlag
	#Lable_ee_Button.configure(state='normal')
def Get_RunONTFlag():
	return GlobalVar.ONT.get('CmdFlag')

def Set_RunHbPort(HbPort):
	GlobalVar.ONT['HbPort'] = HbPort
def Get_RunHbPort():
	return GlobalVar.ONT.get('HbPort')

def Set_RunONTMac(mac):
	GlobalVar.ONT['ONTMac'] = mac
def Get_RunONTMac():
	return GlobalVar.ONT.get('ONTMac')

def Set_RunCmdType(CmdType):
	GlobalVar.ONT['CmdType'] = CmdType
def Get_RunCmdType():
	return GlobalVar.ONT.get('CmdType')
def Set_RunFenFaBoot(FenFaBoot):
	GlobalVar.ONT['FenFaBoot'] = FenFaBoot
def Get_RunFenFaBoot():
	return GlobalVar.ONT.get('FenFaBoot')

def Set_RunFenFaRegister(FenFaRegister):
	GlobalVar.ONT['FenFaRegister'] = FenFaRegister
def Get_RunFenFaRegister():
	return GlobalVar.ONT.get('FenFaRegister')

def Set_RunYunYingBoot(YunYingBoot):
	GlobalVar.ONT['YunYingBoot'] = YunYingBoot
def Get_RunYunYingBoot():
	return GlobalVar.ONT.get('YunYingBoot')

def Set_RunYunYingRegister(YunYingRegister):
	GlobalVar.ONT['YunYingRegister'] = YunYingRegister
def Get_RunYunYingRegister():
	return GlobalVar.ONT.get('YunYingRegister')

def Set_RunHb(Hb):
	GlobalVar.ONT['Hb'] = Hb
def Get_RunHb():
	return GlobalVar.ONT.get('Hb')

def Set_RunYunYingRequestPlug(RequestPlug):
	GlobalVar.ONT['RequestPlug-in'] = RequestPlug
def Get_RunYunYingRequestPlug():
	return GlobalVar.ONT.get('RequestPlug-in')

def Set_RunYunYingRequestDistri(RequestDistri):
	GlobalVar.ONT['RequestDistri'] = RequestDistri
def Get_RunYunYingRequestDistri():
	return GlobalVar.ONT.get('RequestDistri')

def Set_RunChaJianDisconnect(Disconnect):
	GlobalVar.ONT['Disconnect'] = Disconnect
def Get_RunChaJianDisconnect():
	return GlobalVar.ONT.get('Disconnect')
