# -*- coding:utf-8 -*-
from Tkinter import *
from Tkinter import StringVar
import ttk
import win32ui
from TCPandUDP.CmdSwitch import *
from RunningOnu import *
import base64
import win32api
import tkMessageBox

####左侧Frame页面绘图
def LeftFrame_Up(Frame_Left_Up,ListTest):
	global FrameListTest
	FrameListTest = ListTest
	#####--a
	Lable_a = Label(Frame_Left_Up,text='(a)网关向运营平台注册      ',width=20)
	Lable_a.grid(row=0,column=0,sticky= W)
	global Lable_a_list
	Lable_a_list = StringVar()
	Lable_a2= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_a_list)
	Lable_a_list.set("未设置")
	Lable_a2["values"] = ("未设置","返回0同时返回ChallengeCode。","平台响应超时或返回-1。","返回-2时，表示网关提交信息不合法。","返回-5时，网关开始重新注册。")  #注册OLT选择
	Lable_a2.bind("<<ComboboxSelected>>",Get_Lable_a_list)#
	Lable_a2.grid(row=0,column=1,sticky= W)# sticky=(W, E)靠左还是靠右
	###---b
	Lable_b = Label(Frame_Left_Up,text='(b)网关向运营平台注册2    ',width=20)
	Lable_b.grid(row=1,column=0,sticky= W)
	global Lable_b_list
	Lable_b_list = StringVar()
	Lable_b2= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_b_list)
	Lable_b_list.set("未设置")
	Lable_b2["values"] = ("未设置","返回2，UserID相同，","返回3，UserID不相同或不存在","平台响应超时，网关重新发起平台注册。","返回-2时，静默150分钟","返回-5时，网关开始重新注册。")  #注册OLT选择
	Lable_b2.bind("<<ComboboxSelected>>",Get_Lable_b_list)
	Lable_b2.grid(row=1,column=1,sticky= W)# sticky=(W, W)靠左还是靠右
	###---c
	Lable_c = Label(Frame_Left_Up,text='(c)心跳保活                     ',width=20)
	global Lable_c_list
	Lable_c_list = StringVar()
	Lable_c2= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_c_list)
	Lable_c_list.set("未设置")
	Lable_c2["values"] = ("未设置","保持正常心跳，间隔30秒","如果30秒内没有收到回复","返回-3,需要网关重新向平台注册","返回-5,网关重新连接其它服务器")  #注册OLT选择
	Lable_c2.bind("<<ComboboxSelected>>",Get_Lable_c_list)
	Lable_c.grid(row=2,column=0,sticky= W)
	Lable_c2.grid(row=2,column=1,sticky= W)# sticky=(W, W)靠左还是靠右
	###---d
	Lable_d = Label(Frame_Left_Up,text='(d)反向触发网关到插件中心',width=20)
	Lable_d.grid(row=3,column=0,sticky= W)
	global Lable_d_list
	Lable_d_list = StringVar()
	Lable_d2= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_d_list)
	Lable_d_list.set("未设置")
	Lable_d2["values"] = ("未设置","正常流程测试","平台返回-1，重新开始网关向平台注册")  #注册OLT选择
	Lable_d2.bind("<<ComboboxSelected>>",Get_Lable_d_list)
	Lable_d2.grid(row=3,column=1,sticky= W)# sticky=(W, W)靠左还是靠右
	###---e
	Lable_e = Label(Frame_Left_Up,text='(e)反向触发网关重新注册   ',width=20)
	Lable_e.grid(row=4,column=0,sticky= W)
	global Lable_e_list
	Lable_e_list = StringVar()
	Lable_e2= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_e_list)
	Lable_e_list.set("未设置")
	Lable_e2["values"] = ("未设置","正常流程测试","平台返回-1，重新开始网关向平台注册")  #注册OLT选择
	Lable_e2.bind("<<ComboboxSelected>>",Get_Lable_e_list)
	Lable_e2.grid(row=4,column=1,sticky= W)# sticky=(W, W)靠左还是靠右
	###---f
	Lable_f = Label(Frame_Left_Up,text='(f)反向触发网关重新注册   ',width=20)
	Lable_f.grid(row=5,column=0,sticky= W)
	global Lable_f_list
	Lable_f_list = StringVar()
	Lable_f2= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_f_list)
	Lable_f_list.set("未设置")
	Lable_f2["values"] = ("未设置","触发网关和插件中心断开连接！")  #注册OLT选择
	Lable_f2.bind("<<ComboboxSelected>>",Get_Lable_f_list)
	Lable_f2.grid(row=5,column=1,sticky= W)# sticky=(W, W)靠左还是靠右
	###---aa
	Lable_aa = Label(Frame_Left_Up,text='(a)网关向分发平台注册  ',width=20)
	Lable_aa.grid(row=0,column=2,sticky= W)
	global Lable_aa_list
	Lable_aa_list = StringVar()
	Lable_aa= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_aa_list)
	Lable_aa_list.set("未设置")
	Lable_aa["values"] = ("未设置","返回0, 连接成功","返回-1，不响应","返回-2，静默150分钟再重新注册")  #注册OLT选择
	Lable_aa.bind("<<ComboboxSelected>>",Get_Lable_aa_list)
	Lable_aa.grid(row=0,column=3,sticky= W)# sticky=(W, W)靠左还是靠右
	###---bb
	Lable_bb = Label(Frame_Left_Up,text='(b)网关向分发平台注册2',width=20)
	Lable_bb.grid(row=1,column=2,sticky= W)
	global Lable_bb_list
	Lable_bb_list = StringVar()
	Lable_bb= ttk.Combobox(Frame_Left_Up,width=30,textvariable=Lable_bb_list)
	Lable_bb_list.set("未设置")
	Lable_bb["values"] = ("未设置","返回2, 连接成功","平台没有响应，终端应用相同服务器端口重试。","运营平台响应超时，网关向分发平台发起平台注册.","返回-2，静默150分钟重新注册")  #注册OLT选择
	Lable_bb.bind("<<ComboboxSelected>>",Get_Lable_bb_list)
	Lable_bb.grid(row=1,column=3,sticky= W)# sticky=(W, W)靠左还是靠右
	###---选择远程命令：
	Lable_dd_Button = Button(Frame_Left_Up,text='选择远程命令',relief="groove",command= OpenCmdListWindows)
	Lable_dd_Button.grid(row=3,column=2)
	global  Lable_cmd_list
	Lable_cmd_list = StringVar()
	Lable_cmd=Entry(Frame_Left_Up,textvariable=Lable_cmd_list,width=28)
	Lable_cmd.grid(row=3,column=3,sticky= W)
	Lable_cmd_list.set('---请选择执行命令---')
	###---打开系统日志
	Lable_dd_Button = Button(Frame_Left_Up,text='打开系统日志',relief="groove",command=OpenCmdLogWindows)
	Lable_dd_Button.grid(row=5,column=2)
	###---开始异常流程测试
	global Lable_ee_Button
	Lable_ee_Button = Button(Frame_Left_Up,text='开始异常流程测试',foreground= "red",relief="groove",state='normal',command=TestButton)
	Lable_ee_Button.grid(row=5,column=3)
	#Lable_ee_Button.configure(state='normal')
	###---清空窗口
	Lable_ee_Button = Button(Frame_Left_Up,text='清空窗口Log',relief="groove",state='normal',command=CleaWindows)
	Lable_ee_Button.grid(row=5,column=4)

####左侧Frame页面中选择远程命令功能、并保存到runningdata数据中去
def OpenCmdListWindows():
	dlg = win32ui.CreateFileDialog(1)
	#print sys.path[0]   			##当前脚本绝对路径
	dlg.SetOFNInitialDir(sys.path[0]+'\ServerCmd')
	dlg.DoModal()
	filename = dlg.GetPathName()
	#print u"获取到远程命令为：",filename
	dataline5= ReadCmdListWindowsDate(filename,5)###第5行为命令
	dataline6 = ReadCmdListWindowsDate(filename,6)###第六行为命令
	if len(dataline6)==0:
		#print u"选择的命令内容为：",dataline6
		Lable_cmd_list.set(Filter(dataline5,':"(.*?)"'))###更新命令名称
		data = dataline5
		Set_RunCmdType(data)
		Set_RunONTFlag(1)								#命令标志位
		print u"远程命令为空，插件中心调试模式",Get_RunCmdType()
	else:
		endataline6 = base64.b64encode(dataline6)
		#print u"选择的命令内容为：",dataline6
		Lable_cmd_list.set(Filter(dataline6,":\"(.*?)\","))###更新命令名称
		data = dataline5+'"'+endataline6+'"'+"}"					##将第六行和第五行组合
		Set_RunCmdType(data)
		Set_RunONTFlag(1)								#命令标志位
		print u"远程命令写入成功",Get_RunCmdType()

####打开系统log路径
def OpenCmdLogWindows():
	#os.system('Log\log.txt')
	win32api.ShellExecute(0, 'open', 'notepad.exe', 'Log\log.txt','',1)  	##两种方式打开记事本文件

###测试按钮，返回GlobalVar.ONT字典中所有元素
def TestButton():
	#if Get_RunONTFlag() == 1:	  ###判断标志位，开始测试命令按钮变为禁用状态
	#	Lable_ee_Button.configure(state='disabled')
	#elif Get_RunONTFlag() == 0:
	#	Lable_ee_Button.configure(state='normal')

	for (k,v) in GlobalVar.ONT.items():
		print '%s:%s' %(k, v)
	cmddata = str(Get_RunCmdType())
	if cmddata != "TestCmdType":
		cmd = re.findall("\"Parameter\":\"(.*?)\"}",cmddata,re.S)
		if len(cmd)==0:
			cmddecode = "None"
		else:
			try:
				cmddecode= base64.b64decode(str(cmd[0]))
			except:IndexError()
	else:
		cmddata = "None"
		cmddecode = "None"
	if tkMessageBox.showinfo("当前配置信息",
						  "当前测试设备:"+ '\t\t'+Get_RunONTMac()+'\n'+
						  "标志位(1为开始测试):"+ '\t\t'+str(Get_RunONTFlag())+'\n'+
						  "a)网关向分发平台注册-BootFirst:"+ '\t'+str(Get_RunFenFaBoot()[1])+'\n'+
						  "b)网关向分发平台注册(2)-RegisterFirst:"+ '\t'+str(Get_RunFenFaRegister()[1])+'\n'+
						  "a)网关向运营平台注册-Boot:"+ '\t\t'+str(Get_RunYunYingBoot()[1])+'\n'+
						  "b)网关向运营平台注册(2)-Register:"+ '\t'+str(Get_RunYunYingRegister()[1])+'\n'+
						  "c)运营平台心跳保活-Hb:"+ '\t\t'+str(Get_RunHb()[1])+'\n'+
						  "d)反向触发网关连接到插件中心-RequestPlug:"+ '\t'+str(Get_RunYunYingRequestPlug()[1])+'\n'+
						  "e)反向触发网关重新注册-RequestDistri:"+ '\t\t'+str(Get_RunYunYingRequestDistri()[1])+'\n'+
						  "f)触发网关和插件中心断开连接-Disconnect:"+ '\t'+str(Get_RunChaJianDisconnect()[1])+'\n'+
						  "发送远程命令："+ '\n\t'+ cmddata+'\n'+
						  "Cmd源码："+'\n\t'+cmddecode):
		CleaWindows()
		Set_RunONTFlag(1)
	else:
		pass

def CleaWindows():
	FrameListTest.delete(1.0, END)
	print u"清空窗口Log"

###(a)网关向分发平台注册
def Get_Lable_aa_list(event):
	#"未设置","返回0, 连接成功","返回-1，不响应","返回-2，静默150分钟再重新注册"
	#print u"(a)网关向分发平台注册",Lable_aa_list.get()
	FenFaBoot = (0,0)
	if Lable_aa_list.get()==u"未设置":
		FenFaBoot = (0,0)
		print u"(a)网关向分发平台注册;[未设置]"
	elif Lable_aa_list.get()==u"返回0, 连接成功":
		FenFaBoot=(0,0)
		print u"(a)网关向分发平台注册;[返回0, 连接成功]"
	elif Lable_aa_list.get()==u"返回-1，不响应":
		FenFaBoot=(0,-1)
		print u"(a)网关向分发平台注册;[返回-1，不响应]"
	elif Lable_aa_list.get()==u"返回-2，静默150分钟再重新注册":
		FenFaBoot=(0,-2)
		print u"(a)网关向分发平台注册;[返回-2，静默150分钟再重新注册]"
	Set_RunFenFaBoot(FenFaBoot)

###(b)网关向分发平台注册2
def Get_Lable_bb_list(event):
	#"未设置","返回2, 连接成功","平台没有响应，终端应用相同服务器端口重试。","运营平台响应超时，网关向分发平台发起平台注册.","返回-2，静默150分钟重新注册"
	#print u"(b)网关向分发平台注册2",Lable_bb_list.get()
	FenFaRegister= (0,2)
	if Lable_bb_list.get()==u"未设置":
		FenFaRegister= (0,2)
		print u"(b)网关向分发平台注册2;[未设置]"
	elif Lable_bb_list.get()==u"返回2, 连接成功":
		FenFaRegister=(0,2)
		print u"(b)网关向分发平台注册2;[返回2, 连接成功]"
	elif Lable_bb_list.get()==u"平台没有响应，终端应用相同服务器端口重试。":
		FenFaRegister=(1,2)
		print u"(b)网关向分发平台注册2;[平台没有响应，终端应用相同服务器端口重试。]"
	elif Lable_bb_list.get()==u"运营平台响应超时，网关向分发平台发起平台注册.":
		FenFaRegister=(2,2)
		print u"(b)网关向分发平台注册2;[运营平台响应超时，网关向分发平台发起平台注册.]"
	elif Lable_bb_list.get()==u"返回-2，静默150分钟重新注册":
		FenFaRegister=(0,-2)
		print u"(b)网关向分发平台注册2;[返回-2，静默150分钟重新注册]"
	Set_RunFenFaRegister(FenFaRegister)

###(a)网关向运营平台注册
def Get_Lable_a_list(event):
	#print u"(a)网关向运营平台注册",Lable_a_list.get()
	#"未设置","返回0同时返回ChallengeCode。","平台响应超时或返回-1。","返回-2时，表示网关提交信息不合法。","返回-5时，网关开始重新注册。"
	YunYingBoot= (0,0)
	if Lable_a_list.get()==u"未设置":
		YunYingBoot= (0,0)
		print u"(a)网关向运营平台注册;[未设置]"
	elif Lable_a_list.get()==u"返回0同时返回ChallengeCode。":
		YunYingBoot= (0,0)
		print u"(a)网关向运营平台注册:[返回0同时返回ChallengeCode。]"
	elif Lable_a_list.get()==u"平台响应超时或返回-1。":
		YunYingBoot= (0,-1)
		print u"(a)网关向运营平台注册:[平台响应超时或返回-1。]"
	elif Lable_a_list.get()==u"返回-2时，表示网关提交信息不合法。":
		YunYingBoot= (0,-2)
		print u"(a)网关向运营平台注册:[返回-2时，表示网关提交信息不合法。]"
	elif Lable_a_list.get()==u"返回-5时，网关开始重新注册。":
		YunYingBoot= (0,-5)
		print u"(a)网关向运营平台注册:[返回-5时，网关开始重新注册。]"
	Set_RunYunYingBoot(YunYingBoot)

###(b)网关向运营平台注册2
def Get_Lable_b_list(event):
	#print u"(b)网关向运营平台注册2",Lable_b_list.get()
	#"未设置","返回2，UserID相同，","返回3，UserID不相同或不存在","平台响应超时，网关重新发起平台注册。","返回-2时，静默150分钟","返回-5时，网关开始重新注册。"
	YunYingRegister = (0,2)
	if Lable_b_list.get()== u"未设置":
		YunYingRegister = (0,2)
		print u"(b)网关向运营平台注册2:[未设置]"
	elif Lable_b_list.get()== u"返回2，UserID相同，":
		YunYingRegister = (0,2)
		print u"(b)网关向运营平台注册2:[返回2，UserID相同，]"
	elif Lable_b_list.get()== u"返回3，UserID不相同或不存在":
		YunYingRegister = (0,3)
		print u"(b)网关向运营平台注册2:[返回3，UserID不相同或不存在]"
	elif Lable_b_list.get()== u"平台响应超时，网关重新发起平台注册。":
		YunYingRegister = (2,0)
		print u"(b)网关向运营平台注册2:[平台响应超时，网关重新发起平台注册。]"
	elif Lable_b_list.get()== u"返回-2时，静默150分钟":
		YunYingRegister = (0,-2)
		print u"(b)网关向运营平台注册2:[返回-2时，静默150分钟]"
	elif Lable_b_list.get()== u"返回-5时，网关开始重新注册。":
		YunYingRegister = (0,-5)
		print u"(b)网关向运营平台注册2:[返回-5时，网关开始重新注册。]"
	Set_RunYunYingRegister(YunYingRegister)

####(c)心跳保活
def Get_Lable_c_list(event):
	#print u"(c)心跳保活 ",Lable_c_list.get()
	#"未设置","保持正常心跳，间隔30秒","如果30秒内没有收到回复","返回-3,需要网关重新向平台注册","返回-5,网关重新连接其它服务器"
	Hb = (0,35)
	if Lable_c_list.get() == u"未设置":
		Hb = (0,35)
		print u"(c)心跳保活;[未设置]"
	elif Lable_c_list.get() == u"保持正常心跳，间隔30秒":
		Hb = (0,30)
		print u"(c)心跳保活;[返回2, 连接成功]"
	elif Lable_c_list.get() == u"如果30秒内没有收到回复":
		Hb = (1,0)
		print u"(c)心跳保活;[如果30秒内没有收到回复]"
	elif Lable_c_list.get() == u"返回-3,需要网关重新向平台注册":
		Hb = (-3,0)
		print u"(c)心跳保活;[返回-3,需要网关重新向平台注册]"
	elif Lable_c_list.get() == u"返回-5,网关重新连接其它服务器":
		Hb = (-5,0)
		print u"(c)心跳保活;[返回-5,网关重新连接其它服务器]"
	Set_RunHb(Hb)

###(d)反向触发网关到插件中心
def Get_Lable_d_list(event):
	#print u"(d)反向触发网关到插件中心",Lable_d_list.get().get()
	#"未设置","正常流程测试","平台返回-1，重新开始网关向平台注册"
	RequestPlug = (0,1)
	if Lable_d_list.get() == u"未设置":
		RequestPlug = (0,1)
		print u"(d)反向触发网关到插件中心;[未设置]"
	elif Lable_d_list.get() == u"正常流程测试":
		RequestPlug = (0,1)
		print u"(d)反向触发网关到插件中心;[正常流程测试]"
	elif Lable_d_list.get() == u"平台返回-1，重新开始网关向平台注册":
		RequestPlug = (0,-1)
		print u"(d)反向触发网关到插件中心;[平台返回-1，重新开始网关向平台注册]"
	Set_RunYunYingRequestPlug(RequestPlug)

###(e)反向触发网关重新注册
def Get_Lable_e_list(event):
	#print u"(e)反向触发网关重新注册",Lable_e_list.get()
	#"未设置","正常流程测试","平台返回-1，重新开始网关向平台注册"
	RequestDistri = (0,0)
	if Lable_e_list.get() == u"未设置":
		RequestDistri = (0,0)
		print u"(e)反向触发网关重新注册;[未设置]"
	elif Lable_e_list.get() == u"正常流程测试":
		RequestDistri = (0,0)
		print u"(e)反向触发网关重新注册;[正常流程测试]"
	elif Lable_e_list.get() == u"平台返回-1，重新开始网关向平台注册":
		RequestDistri = (0,-1)
		print u"(e)反向触发网关重新注册:[平台返回-1，重新开始网关向平台注册]"
	Set_RunYunYingRequestDistri(RequestDistri)

###(f)反向触发网关重新注册
def Get_Lable_f_list(event):
	#print u"(f)反向触发网关重新注册",Lable_f_list.get()
	#"未设置","触发网关和插件中心断开连接！"
	Disconnect = ()
	if Lable_f_list.get() == u"未设置":
		print u"(f)反向触发网关重新注册;[未设置]"
	elif Lable_f_list.get() == u"触发网关和插件中心断开连接！":
		Disconnect = (0,0)
		print u"(f)反向触发网关重新注册;[触发网关和插件中心断开连接]"
	Set_RunChaJianDisconnect(Disconnect)