# -*- coding:utf-8 -*-
from Tkinter import *
from Tkinter import StringVar
import json
import tkMessageBox
from ServerSettings.ReadServerSettings import *
from OnuList.Readonulist import *
from RunningOnu import *
from OnuList.Addonulist import *

###右侧服务器配置
def RightFrame_Up_Button(Frame_Right):
	###---配置服务器
	#Lable_Button = Button(Frame_Right,text='配置服务器 ',width=12,relief="groove",command=CreatWindow_ServerSetting)
	#Lable_Button.grid(row=0,column=0,padx=1,pady=5)
	###---新增测试设备
	#Lable_Button = Button(Frame_Right,text='新增ONU',width=12,relief="groove",command=CreatWindow_AddOnuSetting)
	#Lable_Button.grid(row=1,column=0,padx=1,pady=5)
	###---新增测试设备
	Lable_Button = Button(Frame_Right,text='删除ONU',width=12,relief="groove",command=RightFrame_Button_RemoveOnu)
	Lable_Button.grid(row=0,column=1,padx=1,pady=5)
	###---确认测试设备
	Lable_Button = Button(Frame_Right,text='确认测试设备',width=12,relief="groove",command=RightFrame_Button_GetonuMac)
	Lable_Button.grid(row=0,column=0,padx=1,pady=5)
	####ONU MAC
	global Lable_cc_list
	Lable_cc_list = StringVar()
	Lable_cc = Label(Frame_Right,text='选择设备MAC:',width=12)
	Lable_cc.grid(row=1,column=0,pady=10,sticky= E)
	Lable_cc2=Entry(Frame_Right,textvariable=Lable_cc_list,foreground= "red",width=18)
	Lable_cc2.grid(row=1,column=1,pady=10,sticky= W)

###TopLevel服务器配置页面
def CreatWindow_ServerSetting():
	Window_Server = Toplevel()
	Window_Server.title(u"服务器配置")
	Window_Server.wm_attributes('-topmost',1)##窗口始终置顶  调试用！！！
	Window_Server.attributes("-alpha", 0.85)#窗口透明度15 %
	Window_Server.iconbitmap('icon\\net.ico')        #对话框图标root.iconbitmap('icon\\net.ico')
	Window_Server.resizable(False,False)
	Window_Server.update() # update window ,must do
	curWidth = 280 # get current width
	curHeight = 160# get current height
	scnWidth,scnHeight = Window_Server.maxsize() # get screen width and height
	tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
	Window_Server.geometry(tmpcnf)
	####
	Ipaddr1 = Label(Window_Server, width=8, text="IP地址:")
	Ipaddr1.grid(row=0, column=0, sticky=E)
	global IpAddr
	IpAddr = StringVar()
	IpAddr.set(ReadSettingsLineName(1))
	IpAddrEntry = Entry(Window_Server, width=13, textvariable=IpAddr)
	IpAddrEntry.grid(row=0, column=1, sticky=W)
	#####
	Port1 = Label(Window_Server, width=8, text="分发端口:")
	Port1.grid(row=1, column=0, sticky=E)
	global PortFenFa
	PortFenFa = StringVar()
	PortFenFa.set(ReadSettingsLineName(2))
	PortEntry = Entry(Window_Server,width=13, textvariable=PortFenFa)
	PortEntry.grid(row=1, column=1, sticky=W)
	#####
	Port1 = Label(Window_Server, width=8, text="运营端口:")
	Port1.grid(row=2, column=0, sticky=E)
	global PortYunYing
	PortYunYing = StringVar()
	PortYunYing.set(ReadSettingsLineName(3))
	PortEntry = Entry(Window_Server,width=13, textvariable=PortYunYing)
	PortEntry.grid(row=2, column=1, sticky=W)
	#####
	Port1 = Label(Window_Server, width=8, text="插件端口:")
	Port1.grid(row=3, column=0, sticky=E)
	global PortChaJian
	PortChaJian = StringVar()
	PortChaJian.set(ReadSettingsLineName(4))
	PortEntry = Entry(Window_Server,width=13, textvariable=PortChaJian)
	PortEntry.grid(row=3, column=1, sticky=W)
	####Tcp、Udp Switch
	SwitchTCPUDP = Label(Window_Server, width=8, text="平台开关:")
	SwitchTCPUDP.grid(row=4, column=0, sticky=E)
	global UdpSwitch
	UdpSwitch = IntVar()
	UdpSwitch.set(ReadSettingsLineName(5))
	UdpSwitchButton=Checkbutton(Window_Server,width=6,variable = UdpSwitch,text ="UDP分发")
	UdpSwitchButton.grid(row=4, column=1, sticky=W)
	global TcpSwitch
	TcpSwitch = IntVar()
	TcpSwitch.set(ReadSettingsLineName(6))
	TcpSwitchButton=Checkbutton(Window_Server,width=6,variable = TcpSwitch,text ="TCP分发")
	TcpSwitchButton.grid(row=4, column=2, sticky=W)
	###---保存配置
	Notes = Label(Window_Server,width=24,text="保存配置后请重新开启服务",font=NORMAL,fg = 'red')
	Notes.grid(row=5, column=0,columnspan=2, sticky=E)
	Lable_Button = Button(Window_Server,text='保存配置',relief="groove",command=CreatWindow_ServerSettingsSave)
	Lable_Button.grid(row=5,column=2,sticky=E,padx=20)

###TopLevelONU添加页面
def CreatWindow_AddOnuSetting():
	Window_AddOnu = Toplevel()
	Window_AddOnu.title(u"服务器配置")
	Window_AddOnu.wm_attributes('-topmost',1)##窗口始终置顶  调试用！！！
	Window_AddOnu.attributes("-alpha", 0.85)#窗口透明度15 %
	Window_AddOnu.iconbitmap('icon\\net.ico')          #对话框图标
	Window_AddOnu.resizable(False,False)
	Window_AddOnu.update() # update window ,must do
	curWidth = 250 # get current width
	curHeight = 200# get current height
	scnWidth,scnHeight = Window_AddOnu.maxsize() # get screen width and height
	tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
	Window_AddOnu.geometry(tmpcnf)
	####
	Mode = Label(Window_AddOnu, width=8, text="Mode:")
	Mode.grid(row=0, column=0, sticky=E)
	global ONUMode
	ONUMode = StringVar()
	ONUMode.set('ZXHN F450G')
	IpAddrEntry = Entry(Window_AddOnu, width=25, textvariable=ONUMode)
	IpAddrEntry.grid(row=0, column=1, sticky=W)
	#####
	MAC = Label(Window_AddOnu, width=8, text="MAC:")
	MAC.grid(row=1, column=0, sticky=E)
	global ONUMAC
	ONUMAC = StringVar()
	ONUMAC.set('001122334455')
	PortEntry = Entry(Window_AddOnu,width=25, textvariable=ONUMAC)
	PortEntry.grid(row=1, column=1, sticky=W)
	#####
	SSID = Label(Window_AddOnu, width=8, text="SSID:")
	SSID.grid(row=2, column=0, sticky=E)
	global ONUSSID
	ONUSSID = StringVar()
	ONUSSID.set('ChinaNet-0000')
	PortEntry = Entry(Window_AddOnu,width=25, textvariable=ONUSSID)
	PortEntry.grid(row=2, column=1, sticky=W)
	#####
	SSIDPwd = Label(Window_AddOnu, width=8, text="SSID-Pwd:")
	SSIDPwd.grid(row=3, column=0, sticky=E)
	global ONUSSIDPwd
	ONUSSIDPwd = StringVar()
	ONUSSIDPwd.set('12345678')
	PortEntry = Entry(Window_AddOnu,width=25, textvariable=ONUSSIDPwd)
	PortEntry.grid(row=3, column=1, sticky=W)
	#####
	UserPwd = Label(Window_AddOnu, width=8, text="User-Pwd:")
	UserPwd.grid(row=4, column=0, sticky=E)
	global ONUUserPwd
	ONUUserPwd = StringVar()
	ONUUserPwd.set('12345')
	PortEntry = Entry(Window_AddOnu,width=25, textvariable=ONUUserPwd)
	PortEntry.grid(row=4, column=1, sticky=W)
	#####
	SN = Label(Window_AddOnu, width=8, text="SN:")
	SN.grid(row=5, column=0, sticky=E)
	global ONUSN
	ONUSN = StringVar()
	ONUSN.set('123456-12345001122334455')
	PortEntry = Entry(Window_AddOnu,width=25, textvariable=ONUSN)
	PortEntry.grid(row=5, column=1, sticky=W)
	###---保存配置
	Notes = Label(Window_AddOnu,width=25,text="新增设备后请重新开启服务",font=NORMAL,fg = 'red')
	Notes.grid(row=6, column=0,columnspan=2, sticky=E)
	Lable_Button = Button(Window_AddOnu,text='新增设备',relief="groove",command=CreatWindow_AddOnuSettingsSave)
	Lable_Button.grid(row=7,column=1,sticky=E,pady=5,padx=5)

###TopLevel服务器配置页面中保存按钮
def CreatWindow_ServerSettingsSave():
	NewIpAddr= IpAddr.get()
	NewPortFenFa = PortFenFa.get()
	NewPortYunYing = PortYunYing.get()
	NewPortChaJian = PortChaJian.get()
	UdpFlag=UdpSwitch.get()
	TcpFlag=TcpSwitch.get()
	print NewIpAddr,NewPortFenFa,NewPortYunYing,NewPortChaJian ##保存服务器配置信息
	SaveSettingsLineName(NewIpAddr,NewPortFenFa,NewPortYunYing,NewPortChaJian,UdpFlag,TcpFlag)
	os._exit(0)

def CreatWindow_AddOnuSettingsSave():
	NewONUMode = ONUMode.get()
	NewONUMAC = ONUMAC.get()
	NewONUSSID = ONUSSID.get()
	NewONUSSIDPwd = ONUSSIDPwd.get()
	NewONUUserPwd = ONUUserPwd.get()
	NewONUSN = ONUSN.get()
	if len(NewONUMAC) != 12:
		tkMessageBox.showinfo("错误提示", "MAC地址长度错误！")
	elif len(NewONUSSID)!=13:
		tkMessageBox.showinfo("错误提示", "SSID配置错误！")
	elif len(NewONUSN) !=24:
		print len("60BB0C-3430060BB0C5958F5")
		tkMessageBox.showinfo("错误提示", "SN长度错误！SN长度24位")
	else:
		info = AddOnu(NewONUMode,NewONUMAC,NewONUSSID,NewONUSSIDPwd,NewONUUserPwd,NewONUSN)
		#info 为添加回调信息
		print info
		os._exit(0)
def CreatWindow_About():
	tkMessageBox.showinfo("关于异常能力平台说明", "欢迎使用！该平台是基于Python2.7+Tkinter，同时支持TCP\UDP两种连接方式。支持多设备并发连接，但只能同时测试一台设备。首次使用请配置服务器地址及添加测试设备。")
###ONU List
def RightFrame_Center_Listbox(Frame_Right_Center,Frame_Right_Center_List):
	Frame_Right_Center_List.bind('<ButtonRelease-1>',Get_Right_Listbox_item)
	global lb_list
	lb_list = Frame_Right_Center_List
	#self.Right_List_Flash()
	Frame_Right_Center_List.grid(row=0,column=0,padx=2,pady=5,sticky= W)
	scrl = Scrollbar(Frame_Right_Center)
	scrl.grid(row=0,column=1,padx=2,pady=5,sticky=NS)
	Frame_Right_Center_List.configure(yscrollcommand = scrl.set)
	scrl['command'] = Frame_Right_Center_List.yview
	ct = 0
	count = ReadConfigLineCount()
	onulist = ReadConfigLineData()
	while ct < count:
		onu = onulist[ct][0:12]   #取列表12位MAC地址
		Frame_Right_Center_List.insert(ct,onu)
		ct+=1
###右侧onu信息显示表
def RightFrame_Down__Listbox(Frame_Right_Down_List):
	global lb_onudat
	lb_onudat = Frame_Right_Down_List
	Frame_Right_Down_List.grid(row=0,column=0,padx=2,pady=5,sticky= W)
###右侧onu信息信息更新
def Get_Right_Listbox_item(event):
	print u"当前list行中命令位置",lb_list.curselection()[0],u"列表中名称",lb_list.get(lb_list.curselection())
	Lable_cc_list.set(lb_list.get(lb_list.curselection()))			###选择的设备mac
	onuDate = ReadConfigOnuData(lb_list.get(lb_list.curselection()))
	ansDate = json.loads(onuDate)
	serMode=ansDate['Mode']
	lb_onudat.delete(0,END)  ####列表onu信息清空
	lb_onudat.insert(1,"Mode:"+serMode)
	serMAC=ansDate['MAC']
	lb_onudat.insert(2,"MAC:"+serMAC)
	serSSID=ansDate['SSID']
	lb_onudat.insert(3,"SSID:"+serSSID)
	serSSIDPwd=ansDate['SSID-Pwd']
	lb_onudat.insert(4,"SSID-Pwd:"+serSSIDPwd)
	seruserPwd=ansDate['user-Pwd']
	lb_onudat.insert(5,"user-Pwd:"+seruserPwd)
	serSN=ansDate['SN']
	lb_onudat.insert(6,"SN:"+serSN)

###右侧按钮“确认测试设备”功能
def RightFrame_Button_GetonuMac():
	try:
		print u"当前选择设备为：",lb_list.get(lb_list.curselection())
		OnuMac = lb_list.get(lb_list.curselection())
	except:
		TclError()
		OnuMac = None
	Set_RunONTMac(OnuMac)
	print u"ONTMac写入成功",Get_RunONTMac()

###右侧按钮“删除ONU”功能
def RightFrame_Button_RemoveOnu():
	print u"当前选择设备为：",lb_list.get(lb_list.curselection())
	OnuMac = lb_list.get(lb_list.curselection())
	RemoveOnu(OnuMac)






