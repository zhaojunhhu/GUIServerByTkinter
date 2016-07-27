# -*- coding:utf-8 -*-
import linecache
import re
import os
######正则表达式过滤内容
def Filter(strs,guize):    ###正则表达式过滤内容
    myItems = re.findall(guize,strs,re.S)
    Items = ''.join(myItems)
    return Items

###serversettings中配置IP、port等信息
def ReadSettingsLineName(Num):    #获取要查询的“命令”标题
    s = linecache.getline("ServerSettings\serversetting.ini",Num)
    linecache.clearcache()         #很关键的一句，否则listbox调用时会刷新
    lineName=Filter(s,":\"(.*?)\"}")
    return lineName

###保存serversettings中配置IP、port等信息
def SaveSettingsLineName(NewIpAddr,NewPortFenFa,NewPortYunYing,NewPortChaJian,FenFaUDP,FenFaTCP):    #获取要查询的“命令”标题
    S = open("ServerSettings\serversetting.ini",'w')
    #dat = '--ServerIP--={"IP":"61.172.62.245"}--ServerPort_Fenfa={"Port":"12112"}--ServerPort_Yunying={"Port":"60001"}--ServerPort_Chajian={"Port":"60002"}'
    ServerIP = '--ServerIP--={"IP":"'+str(NewIpAddr)+'"}\n'
    ServerPort_Fenfa = '--ServerPort_Fenfa={"Port":"'+str(NewPortFenFa)+'"}\n'
    ServerPort_Yunying = '--ServerPort_Yunying={"Port":"'+str(NewPortYunYing)+'"}\n'
    ServerPort_Chajian = '--ServerPort_Chajian={"Port":"'+str(NewPortChaJian)+'"}\n'
    ServerFenFaUdp = '--ServerFenFaUdp={"Enable":"'+str(FenFaUDP)+'"}\n'
    ServerFenFaTcp = '--ServerFenFaTcp={"Enable":"'+str(FenFaTCP)+'"}\n'
    ServerDjangoWeb = '--ServerPort_DjangoWeb={"Port":"60006"}\n'
    try:
        S.write(ServerIP)
        S.write(ServerPort_Fenfa)
        S.write(ServerPort_Yunying)
        S.write(ServerPort_Chajian)
        S.write(ServerFenFaUdp)
        S.write(ServerFenFaTcp)
        S.write(ServerDjangoWeb)
    finally:
       S.close( )