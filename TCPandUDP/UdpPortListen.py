# -*- coding:utf-8 -*-
import threading
from Tkinter import *
from socket import *

from CmdSwitch import *
from Log.SaveLog import *
from CmdSet import *
from RunningOnu import *
from djangoweb import *
from OnuList.Addonulist import AddOnu
###UDP  socket port 12112配置
mysocketUDP_Fenfa = socket(AF_INET,SOCK_DGRAM)#SOCK_STREAM)# SOCK_DGRAM)
mysocketUDP_Fenfa.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)	##这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
mysocketUDP_Fenfa.bind(('192.168.10.10', int(ReadSettingsLineName(2))))	#监听IP	端口12112

###UDP  socket port 60001配置
mysocketUDP_Yunying = socket(AF_INET,SOCK_DGRAM)#SOCK_STREAM)# SOCK_DGRAM)
mysocketUDP_Yunying.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)	##这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
mysocketUDP_Yunying.bind(('192.168.10.10', int(ReadSettingsLineName(3))))	#监听IP	端口60001

###UDP  socket WebServer 31500配置
mysocketUDP_WebServer = socket(AF_INET,SOCK_DGRAM)#SOCK_STREAM)# SOCK_DGRAM)
mysocketUDP_WebServer.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)	##这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
mysocketUDP_WebServer.bind(('0.0.0.0', int(ReadSettingsLineName(7))))	#监听IP	端口60001


####UDP链接线程处理12112端口数据
class ListenthreadUDP_Fenfa(threading.Thread):
	def __init__(self,Windows):
		threading.Thread.__init__(self)
		self.List=Windows.Frame_Left_Down_List
	def run(self):
		while True:
			data,ip= mysocketUDP_Fenfa.recvfrom(4096)
			self.List.insert(END, '%s<<<<--From IP :%s--RevcUDP :\n%s\n\n'%(datetime.datetime.now(),ip[0],data))
			AddRecv_UdpLogs(data,ip) ###接收到的消息添加到LOG记录
			if MCSEOnuMac(data) == True:  ##用MAC去判断设备是否存在
				if MCSEOnuTestting(data):	##查询设备是否为当前测试的设备
						print u"当前设备为测试设备"
						if RPCMethod_BootFirst(data) == 'BootFirst':
							print u"当前设备FenFaBoot设置参数为",Get_RunFenFaBoot()
							if Get_RunFenFaBoot()[0] ==0:
								print u"UDP分发平台需要响应它"
								Messages = SendBootFirst(Get_RunFenFaBoot()[1]) ##生成消息，因为消息中32位随机值，所以统一发送
								mysocketUDP_Fenfa.sendto(Messages,ip)	     ##发送BootFirst响应消息
								self.List.insert(END,AddSend_UdpLogs(Messages))  ##插入显示并写入log
								Set_RunFenFaBoot((0,0))                                                    ##异常测试值复位操作
							elif Get_RunFenFaBoot()[0] ==1:	##不响应
								continue
						elif RPCMethod_RegisterFirst(data) == 'RegisterFirst':
							SaveOnuCheckSN(data)		###保存上报的onu CheckSn
							print u"当前设备FenFaRegister设置参数为",Get_RunFenFaRegister()
							if Get_RunFenFaRegister()[0] == 0:
								mysocketUDP_Fenfa.sendto(SendRegisterFirst(60,Get_RunFenFaRegister()[1]),ip)      ##发送RegisterFirst响应消息
								self.List.insert(END,AddSend_UdpLogs(SendRegisterFirst(60,Get_RunFenFaRegister()[1]))) ##插入显示并写入log
								Set_RunFenFaRegister((0,2))                                                          ##异常测试值复位操作
							elif Get_RunFenFaRegister()[0] == 1:	##不响应
								continue
							elif Get_RunFenFaRegister()[0] == 2:	##平台响应超时
								continue
						print u"UDP端口12112收到数据"+data
				else:
					print u"当前设备不属于测试设备"
					if RPCMethod_BootFirst(data):
						Messages = SendBootFirst(0) ##生成消息，因为消息中32位随机值，所以统一发送
						mysocketUDP_Fenfa.sendto(Messages,ip)	  ##发送BootFirst响应消息
						self.List.insert(END,AddSend_UdpLogs(Messages))  ##插入显示并写入log
					elif RPCMethod_RegisterFirst(data):
						SaveOnuCheckSN(data)		###保存上报的onu CheckSn
						mysocketUDP_Fenfa.sendto(SendRegisterFirst(60,2),ip)##发送RegisterFirst响应消息
						self.List.insert(END,AddSend_UdpLogs(SendRegisterFirst(60,2)))##插入显示并写入log
			else:
				mysocketUDP_Fenfa.sendto(SendBootFirst(-6),ip)	##-1 一般失败，-6 MAC不合法
				self.List.insert(END, AddSend_UdpLogs(SendBootFirst(-6)))
			print u"UDP端口12112收到数据"+data

####UDP链接线程处理60001端口数据
class ListenthreadUDP_YunYing(threading.Thread):
	def __init__(self,Windows):
		threading.Thread.__init__(self)
		self.List=Windows.Frame_Left_Down_List
	def run(self):
		while True:
			data,ip= mysocketUDP_Yunying.recvfrom(4096)
			self.List.insert(END, '%s<<<--From IP :%s--RevcUDP :\n%s\n\n'%(datetime.datetime.now(),ip[0],data))
			AddRecv_UdpLogs(data,ip)	###接收到的消息添加到LOG记录
			if MCSEOnuTestting(data) == True :	##查询设备是否为当前测试的设备
					print u"当前设备为测试设备"
					if RPCMethod_Boot(data) == 'Boot':
						print u"当前设备YunYingBoot设置参数为",Get_RunYunYingBoot()
						if Get_RunYunYingBoot()[0] == 0:
							print u"UDP运营平台需要响应它"
							Messages = SendBoot(Get_RunYunYingBoot()[1],35,"1") ##生成消息，因为消息中32位随机值，所以统一发送
							mysocketUDP_Yunying.sendto(Messages,ip)        ##发送BOOT响应消息
							self.List.insert(END,AddSend_UdpLogs(Messages))     ##插入显示并写入log
							Set_RunYunYingBoot((0,0))                                                        ##异常测试值复位操作
						elif Get_RunYunYingBoot()[0] == 1:##不响应
							continue
					elif RPCMethod_Register(data) == 'Register':
						SaveOnuDevRND(data)		###保存设备上报的DevRBD
						print u"当前设备YunYingRegister设置参数为",Get_RunYunYingRegister()
						if Get_RunYunYingRegister()[0] == 0:
							mysocketUDP_Yunying.sendto(SendRegister(Get_RunYunYingRegister()[1]),ip)        ##发送Register响应消息
							self.List.insert(END,AddSend_UdpLogs(SendRegister(Get_RunYunYingRegister()[1])))     ##插入显示并写入log
							Set_RunYunYingRegister((0,2))                                                    ##异常测试值复位操作
						elif Get_RunYunYingRegister()[0] == 1:##不响应
								continue
						elif Get_RunYunYingRegister()[0] == 2:##平台响应超时
								continue
					elif RPCMethod_Hb(data)=='Hb_FLAG1':
							print u"当前设备Hb设置参数为",Get_RunHb()
							mysocketUDP_Yunying.sendto(SendHb(Get_RunHb()[0],Get_RunHb()[1]),ip)            ##发送Hb心跳响应消息
							self.List.insert(END,AddSend_UdpLogs(SendHb(Get_RunHb()[0],Get_RunHb()[1])))         ##插入显示并写入log
							Set_RunHb((0,35))                                                                 ##异常测试值复位操作
							print u"=======================反响触发插件中心=============================="
							mysocketUDP_Yunying.sendto(SendRequestPlug(data),ip)
							self.List.insert(END,AddSend_UdpLogs(SendRequestPlug(data)))##插入显示并写入log
							Set_RunHbPort(ip[1])                                                              ##写入HbPort端口号
							print u"**************************************************HbPort",ip[1]
					elif RPCMethod_Hb(data)=='Hb_FLAG0':
							print u"当前设备Hb设置参数为",Get_RunHb()
							mysocketUDP_Yunying.sendto(SendHb(Get_RunHb()[0],Get_RunHb()[1]),ip)             ##发送Hb心跳响应消息
							self.List.insert(END,AddSend_UdpLogs(SendHb(Get_RunHb()[0],Get_RunHb()[1])))          ##插入显示并写入log
							Set_RunHb((0,35))                                                                  ##异常测试值复位操作
					print u"UDP端口60001收到数据"+data
			elif MCSEOnuTestting(data) == False:
				print u"当前设备不属于测试设备"
				if RPCMethod_Boot(data) == 'Boot':
						Messages = SendBoot(0,35,"1") ##生成消息，因为消息中32位随机值，所以统一发送
						mysocketUDP_Yunying.sendto(Messages,ip)##发送BOOT响应消息
						self.List.insert(END,AddSend_UdpLogs(Messages))##插入显示并写入log
				elif RPCMethod_Register(data) == 'Register':
						SaveOnuDevRND(data)		###保存设备上报的DevRBD
						mysocketUDP_Yunying.sendto(SendRegister(2),ip)##发送Register响应消息
						self.List.insert(END,AddSend_UdpLogs(SendRegister(2)))##插入显示并写入log
				elif RPCMethod_Hb(data)=='Hb_FLAG1':
						print u"*^*^*^*^*首次上报Flag 1，心跳中*^*^*^*^*"
						mysocketUDP_Yunying.sendto(SendHb(0,35),ip)##发送Hb心跳响应消息
						self.List.insert(END,AddSend_UdpLogs(SendHb(0,35)))##插入显示并写入log
						print u"=======================反响触发插件中心=============================="
						mysocketUDP_Yunying.sendto(SendRequestPlug(data),ip)
						self.List.insert(END,AddSend_UdpLogs(SendRequestPlug(data)))##插入显示并写入log
				elif RPCMethod_Hb(data)=='Hb_FLAG0':
						print u"*^*^*^*^*心跳中*^*^*^*^*"
						mysocketUDP_Yunying.sendto(SendHb(0,35),ip)##发送Hb心跳响应消息
						self.List.insert(END,AddSend_UdpLogs(SendHb(0,35)))##插入显示并写入log
				elif RPCMethod_Hb1(data)=='Result0':
						print u"*^*^*^*^*反向触发插件响应*^*^*^*^*"
						if Get_RunHbPort() == ip[1]:
							print u"**************************************************HbPort",ip[1]
							mysocketUDP_Yunying.sendto(SendHb1(Get_RunYunYingRequestPlug()[1]),ip)           ##发送Hb心跳响应消息
							self.List.insert(END,AddSend_UdpLogs(SendHb1(Get_RunYunYingRequestPlug()[1])))        ##插入显示并写入log
							Set_RunYunYingRequestPlug((0,1))                                                  ##异常测试值复位操作
							Set_RunHbPort(0)
						elif Get_RunHbPort() == 0:
							mysocketUDP_Yunying.sendto(SendHb1(1),ip)##发送Hb心跳响应消息
							self.List.insert(END,AddSend_UdpLogs(SendHb1(1)))##插入显示并写入log
				else:
						print u"查询消息类型失败"
			else :
				print u"UDP端口60001收到数据"+data


####UDP链接线程处理60006端口数据
class ListenthreadUDP_WebServer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			data,ip= mysocketUDP_WebServer.recvfrom(1024)
			if  WebMethod(data) =="FindOnu":  ###web页面“新增测试设备”查询设备
				if WebDjangoOnuAddr(data):
					info = 'None'
					try:
						info = WebDjangoFindOnuInfo(data)
					finally:
						mysocketUDP_WebServer.sendto(info,ip)
				else:
					info ={"Result":"-2"}
					info = json.dumps(info)
					mysocketUDP_WebServer.sendto(info,ip)
			elif  WebMethod(data) =="AddOnu": ###web页面“新增测试设备”增加网关
				ans = json.loads(data)
				onuinfo = ans["data"]
				info = 'None'
				try:
					info = AddOnu(onuinfo["Mode"],onuinfo["Mac"],onuinfo["SSID"],onuinfo["SSID-Pwd"],onuinfo["User-Pwd"],onuinfo["SN"])
				finally:
					mysocketUDP_WebServer.sendto(info,ip)
			elif  WebMethod(data) =="OnuRun": ###web页面“平台对接测试
				if WebDjangoOnuAddr(data):
					info = 'None'
					try:
						info = WebDjangoOnuRunInfo(data)
					finally:
						mysocketUDP_WebServer.sendto(info,ip)
				else:
					info ={"Result":"-2"}
					info = json.dumps(info)
					mysocketUDP_WebServer.sendto(info,ip)
			elif  WebMethod(data) =="TestOnu":###web页面“网关能力测试”
				if WebDjangoOnuAddr(data):
					info = 'None'
					try:
						info = WebDjangoTestOnuInfo(data)
					finally:
						mysocketUDP_WebServer.sendto(info,ip)
				else:
					info ={"Result":"-2"}
					info = json.dumps(info)
					mysocketUDP_WebServer.sendto(info,ip)
			elif WebMethod(data) =="GetTestOnuInfo":###web页面“获取服务器快照”
				if WebDjangoOnuAddr(data):
					print "GetTestOnuInfo"
					info = 'None'
					try:
						info = WebDjangoGetTestOnuInfo(data)
					finally:
						mysocketUDP_WebServer.sendto(info,ip)
				else:
					info ={"Result":"-2"}
					info = json.dumps(info)
					mysocketUDP_WebServer.sendto(info,ip)
			else:
				print u"webserver端口60006收到数据"+data
			AddRecv_UdpLogs("From Webserver addonu requeset"+data,ip)	###接收到的消息添加到LOG记录

