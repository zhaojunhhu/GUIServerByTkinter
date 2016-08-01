# -*- coding:utf-8 -*-
from TkGUI.LeftFrame import *
from TkGUI.RightFrame import *
from  TCPandUDP.UdpPortListen import *
from  TCPandUDP.TcpPortListen import *

root = Tk()
root.title("智能网关异常能力平台")
menubar = Menu(root)
root.wm_attributes('-topmost',0)##窗口始终置顶  调试用！！！
root.attributes("-alpha", 0.92)#窗口透明度15 %
root.iconbitmap('icon\\net.ico')        #对话框图标
root.resizable(False,False)
root.update() # update window ,must do
curWidth = 1095 # get current width
curHeight = 700# get current height
scnWidth,scnHeight = root.maxsize() # get screen width and height
root.minsize(900, 640)		##主窗口最小尺寸
tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
root.geometry(tmpcnf)

###进程守护，监控退出按钮
def printProtocol():
	result = tkMessageBox.askyesno("提示","确认程序退出？")
	if result == True:
		print u"程序关闭！！"
		root.destroy()#root退出循环
		os._exit(0)#直接退出 Python 解释器，其后的代码都不执行
	else:
		pass

class MainTk:
	def __init__(self,win):
		self.Frame = Label(win ,width=1090,height=680)#,image=background_image)
		self.Frame.place(x=0, y=0, relwidth=1, relheight=1)
		self.Frame.grid(row=0,column=0)
		###床架左右两个Frame
		self.Frame_Left = Frame(self.Frame,width=550,height=640)
		self.Frame_Right = Frame(self.Frame,width=250,height=640)
		self.Frame_Left.grid(row=0,column=0)
		self.Frame_Right.grid(row=0,column=1,rowspan=2)
		###左侧Frame划分上下两部分，下部分用于info显示
		self.Frame_Left_Up = Frame(self.Frame_Left,width=800,height=300)
		self.Frame_Left_Down = Frame(self.Frame_Left,width=800,height=340)
		self.Frame_Left_Up.grid(row=0,column=0)
		self.Frame_Left_Down.grid(row=1,column=0,columnspan=4)
		##右侧Frame框架划分为三部分。上部为开启，中部为onuList表单，下部分为OnuCmd列表
		self.Frame_Right_Up = Frame(self.Frame_Right,width=250,height=160)
		self.Frame_Right_Center = Frame(self.Frame_Right,width=250,height=400)
		self.Frame_Right_Down = Frame(self.Frame_Right,width=250,height=100)
		self.Frame_Right_Up.grid(row=0,column=0,)
		self.Frame_Right_Center.grid(row=1,column=0)
		self.Frame_Right_Down.grid(row=2,column=0)
		###Right_Center_List
		self.Frame_Right_Center_List = Listbox(self.Frame_Right_Center, height=38,width=32,selectmode =  BROWSE)
		self.Frame_Right_Center.grid_propagate(0)
		###Right_Down_List
		self.Frame_Right_Down_List = Listbox(self.Frame_Right_Down, height=6,width=32)
		self.Frame_Right_Up.grid_propagate(0)
		self.Frame_Right_Down.grid_propagate(0)
		###Left down List
		self.Frame_Left_Down_List = Text(self.Frame_Left_Down,width=120,height=40)
		self.Frame_Left_Down_List.grid(row=0,column=0)
		self.Frame_Left_Down_List.grid_propagate(0)
		###Left down List绑定事件
		self.Frame_Left_Down_List.bind("<Control-Key-a>", self.selectText)
		self.Frame_Left_Down_List.bind("<Control-Key-A>", self.selectText)
		##Left down ListScrl
		self.Frame_Left_Down_scrl = Scrollbar(self.Frame_Left_Down)
		self.Frame_Left_Down_scrl.grid(row=0,column=1,sticky=NS)#,padx=2,pady=5
		self.Frame_Left_Down_List.configure(yscrollcommand = self.Frame_Left_Down_scrl.set)
		self.Frame_Left_Down_scrl['command'] = self.Frame_Left_Down_List.yview
		win.protocol('WM_DELETE_WINDOW',printProtocol)
#####文本全选
	def selectText(self, event):
		self.Frame_Left_Down_List.tag_add(SEL, "1.0",END)
		#self.lfc_field_1_t.mark_set(Tkinter.INSERT, "1.0")
		#self.lfc_field_1_t.see(Tkinter.INSERT)
		return 'break'  #为什么要return 'break'
#####主菜单的menu菜单
	def MainMenu(self,menubar):
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="服务器配置",command=CreatWindow_ServerSetting)
		filemenu.add_separator()
		filemenu.add_command(label="ONU设备管理",command=CreatWindow_AddOnuSetting)
		#filemenu.add_command(label="退出", command=menubar.quit())
		menubar.add_cascade(label="设置", menu=filemenu)
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="关于", command=CreatWindow_About)
		menubar.add_cascade(label="帮助", menu=helpmenu)
#####主程序循环
	def MainLoop(self):
		LeftFrame_Up(self.Frame_Left_Up,self.Frame_Left_Down_List)
		RightFrame_Up_Button(self.Frame_Right_Up)
		RightFrame_Center_Listbox(self.Frame_Right_Center,self.Frame_Right_Center_List)
		RightFrame_Down__Listbox(self.Frame_Right_Down_List)

MyWindows = MainTk(root)
MyWindows.MainMenu(menubar)
root.config(menu=menubar)

lt_UDP_Fenfa = ListenthreadUDP_Fenfa(MyWindows)		##UDP 分发端口12112
lt_UDP_YunYing = ListenthreadUDP_YunYing(MyWindows) ##UDP 分发端口60001
lt_UDP_WebServer = ListenthreadUDP_WebServer()
lt_TCP_Fenfa = ListenthreadTCP_Fenfa()		##TCP 分发端口12112
lt_TCP_YunYing = ListenthreadTCP_YunYing()		##TCP 运营端口60001
lt_TCP_ChaJian = ListenthreadTCP_ChaJian(MyWindows)			##TCP 插件端口60002

#lt_UDP_Fenfa .setDaemon(True)#设置线程为“守护线程”在没有用户线程可服务时会自动离开。
#lt_UDP_YunYing .setDaemon(True)
if ReadSettingsLineName(5) == "1": #开启UDP、TCP各个线程
	lt_UDP_Fenfa.start()
	lt_UDP_YunYing.start()
#elif ReadSettingsLineName(6) == "1":
lt_TCP_Fenfa.start()
lt_TCP_YunYing.start()

lt_TCP_ChaJian.start()
lt_UDP_WebServer.start()

MyWindows.MainLoop()
root.protocol('WM_DELETE_WINDOW',printProtocol)
root.mainloop()