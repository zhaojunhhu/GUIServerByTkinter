# -*- coding:utf-8 -*-
import threading
from Tkinter import *
from SocketServer import BaseRequestHandler,ThreadingTCPServer
import traceback
from CmdSwitch import *
from Log.SaveLog import *
from CmdSet import *
import tkMessageBox

####TCP链接线程处理12112端口数据
class ListenthreadTCP_Fenfa(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		##监控12112端口，引入TCP处理类
		server = ThreadingTCPServer(('192.168.0.10', int(ReadSettingsLineName(2))), MyBaseRequestHandlerrTCP_Fenfa)
		server.serve_forever()

####TCP链接线程处理60001端口数据
class ListenthreadTCP_YunYing(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		server = ThreadingTCPServer(('192.168.0.10', int(ReadSettingsLineName(3))), MyBaseRequestHandlerrTCP_YunYing)
		server.serve_forever()

####TCP链接线程处理60002端口数据
class ListenthreadTCP_ChaJian(threading.Thread):
	def __init__(self,Windows):
		threading.Thread.__init__(self)
		self.List=Windows.Frame_Left_Down_List
	def run(self):
		global List
		List =self.List   #讲Tkinter界面传入
		server = ThreadingTCPServer(('192.168.0.10', int(ReadSettingsLineName(4))), MyBaseRequestHandlerrTCP_ChaJian)
		server.serve_forever()

####TCPServer处理12112端口数据
class MyBaseRequestHandlerrTCP_Fenfa(BaseRequestHandler):
	def handle(self):
		#循环监听（读取）来自客户端的数据
		while True:
			#当客户端主动断开连接时，self.recv(1024)会抛出异常
			try:
				#一次读取1024字节,并去除两端的空白字符(包括空格,TAB,\r,\n)
				data = self.request.recv(4096)
				if not data:
					server.shutdown()
				data = data[4:]
				List.insert(END, '%s<<<<--From IP :%s--RevcTCP :\n%s\n\n'%(datetime.datetime.now(),self.client_address[0],data))
				AddRecv_TcpLogs(data)
				if MCSEOnuMac(data):  ##用MAC去判断设备是否存在
					if RPCMethod_BootFirst(data) == 'BootFirst':
						Messages = SendBootFirst(0) ##生成消息，因为消息中32位随机值，所以统一发送
						self.request.sendall(TCP_Send(Messages))	##发送BootFirst响应消息
						List.insert(END,AddSend_TcpLogs(Messages))	##插入显示并写入log
					elif RPCMethod_RegisterFirst(data) == 'RegisterFirst':
						SaveOnuCheckSN(data)		###保存上报的onu CheckSn
						self.request.sendall(TCP_Send(SendRegisterFirst(60,2)))		##发送RegisterFirst响应消息
						List.insert(END,AddSend_TcpLogs(SendRegisterFirst(60,2)))	##插入显示并写入log
				else:
					self.request.sendall(TCP_Send(SendBootFirst(-6)))	##-1 一般失败，-6 MAC不合法
					List.insert(END,AddSend_TcpLogs(SendBootFirst(-6)))
				print u"TCP端口12112收到数据", data
			except:
				traceback.print_exc()
				break
####TCPServer处理60001端口数据
class MyBaseRequestHandlerrTCP_YunYing(BaseRequestHandler):
	def handle(self):
		#循环监听（读取）来自客户端的数据
		while True:
			#当客户端主动断开连接时，self.recv(1024)会抛出异常
			try:
				#一次读取1024字节,并去除两端的空白字符(包括空格,TAB,\r,\n)
				data = self.request.recv(4096)
				if not data:
					server.shutdown()
				data = data[4:]
				List.insert(END, '%s<<<<--From IP :%s--RevcTCP :\n%s\n\n'%(datetime.datetime.now(),self.client_address[0],data))
				AddRecv_TcpLogs(data)
				if RPCMethod_Boot(data) == 'Boot':
					Messages = SendBoot(0,35,"1") ##生成消息，因为消息中32位随机值，所以统一发送
					self.request.sendall(TCP_Send(Messages))		##发送BOOT响应消息
					List.insert(END,AddSend_TcpLogs(Messages))	##插入显示并写入log
				elif RPCMethod_Register(data) == 'Register':
					SaveOnuDevRND(data)		###保存设备上报的DevRBD
					self.request.sendall(TCP_Send(SendRegister(2)))			##发送Register响应消息
					List.insert(END,AddSend_TcpLogs(SendRegister(2)))
				elif RPCMethod_Hb(data) == 'Hb_FLAG1':
					print u"*^*^*^*^*首次上报Flag 1，心跳中*^*^*^*^*"
					self.request.sendall(TCP_Send(SendHb(0,35)))		##发送Hb心跳响应消息
					List.insert(END,AddSend_TcpLogs(SendHb(0,35)))
				elif RPCMethod_Hb(data) == 'Hb_FLAG0':
					print u"*^*^*^*^*心跳中*^*^*^*^*"
					self.request.sendall(TCP_Send(SendHb(0,35)))		##发送Hb心跳响应消息
					List.insert(END,AddSend_TcpLogs(SendHb(0,35)))
				print u"TCP端口60001收到数据"+data
			except:
				traceback.print_exc()
				break
####TCPServer处理60001端口数据
class MyBaseRequestHandlerrTCP_ChaJian(BaseRequestHandler):
	def handle(self):
		#循环监听（读取）来自客户端的数据
		while True:
			#当客户端主动断开连接时，self.recv(1024)会抛出异常
			try:
				data = self.request.recv(4096)              ###一次读取1024字节,并去除两端的空白字符(包括空格,TAB,\r,\n)
				if not data:
					server.shutdown()
				data = data[4:]
				List.insert(END, '%s<<<<--From IP :%s--RevcTCP :\n%s\n\n'%(datetime.datetime.now(),self.client_address[0],data))
				AddRecv_TcpLogs(data)
				#if MCSEOnuTestting(data):	##查询设备是否为当前测试的设备
				#print u"当前设备为测试设备"
				if RPCMethod_ChaJianBoot(data) == 'Boot':
					print u"设备连接至插件中心"
					Messages = SendChaJianBoot(0) ##生成消息，因为消息中32位随机值，所以统一发送
					self.request.sendall(TCP_Send(Messages))		##发送BOOT响应消息
					List.insert(END,AddSend_TcpLogs(Messages))	##插入显示并写入log
				elif RPCMethod_ChaJianRegister(data) == 'Register':
					self.request.sendall(TCP_Send(SendChaJianRegister(0)))			##发送Register响应消息
					List.insert(END,AddSend_TcpLogs(SendChaJianRegister(0)))
				elif RPCMethod_ChaJianHeartbeat(data) == 'Heartbeat':
					print u"TCP插件中心*^*^*^*^*心跳中*^*^*^*^*"
					self.request.sendall(TCP_Send(SendChaJianHeartbeat(0)))			##发送Register响应消息
					List.insert(END,AddSend_TcpLogs(SendChaJianHeartbeat(0)))
					if Get_RunONTFlag() == 1:
						print  "Get_RunChaJianDisconnect()"
						if Get_RunCmdType()!="TestCmdType":
							print u"TCP插件中心反向触发网关*^*^*^*^*Parameter"
							self.request.sendall(TCP_Send(Get_RunCmdType()))			##发送Register响应消息
							List.insert(END,AddSend_TcpLogs(Get_RunCmdType()))
							Set_RunCmdType("TestCmdType")
						elif Get_RunChaJianDisconnect()[1] == 1:
							print u"TCP插件中心反向触发网关Disconnect断开连接"
							self.request.sendall(TCP_Send(SendChaJianDisconnect()))			##发送Register响应消息
							List.insert(END,AddSend_TcpLogs(SendChaJianDisconnect()))
						else:
							continue                                               ####消息复位
				elif RPCMethod_ChaJianParameter(data) == 'return_Parameter':
					print "异常流程测试完毕！！"
					Set_RunONTFlag(0)
				else:
					print u"查询消息类型失败"
				print u"TCP端口60002收到数据"+data
			except:
				traceback.print_exc()
				break