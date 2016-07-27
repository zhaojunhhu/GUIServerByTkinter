# -*- coding:utf-8 -*-
import linecache
import os
import re
import json
######正则表达式过滤内容
def Filter(strs,guize):    ###正则表达式过滤内容
    myItems = re.findall(guize,strs,re.S)
    Items = ''.join(myItems)
    return Items

###查询设备是否存在onulist。ini中
def Serche_OnuList(file_str):
    file_str = file_str + '.ini'###查找文件名
    dir_name = os.listdir("OnuList\List")
    count = len(dir_name)
    for i in range(0,count):
        if file_str == dir_name[i]:
            return True #设备已经被录入
        else:
            continue

###返回当前onulist行数
def ReadConfigLineCount():
    dir_name = os.listdir("OnuList\List")
    count = len(dir_name)  #返回文件的行数
    return count

####获取onulist指定行中设备MAC
def ReadConfigLineName(Num):    #获取要查询的“命令”标题
    s = linecache.getline("OnuList\onulist.ini",Num)
    linecache.clearcache()         #很关键的一句，否则listbox调用时会刷新
    lineName=Filter(s,"--(.*?)--")
    return lineName

###返回List文件夹中所有文件名称
def ReadConfigLineData():    #获取执行“命令”内容
    dir_name = os.listdir("OnuList\List")
    return dir_name

###返回读取的List中指定ONU信息，入口ONU文件名
def ReadConfigOnuData(OnuMac):
    s = linecache.getline("OnuList\List\\"+OnuMac+".ini",1)
    linecache.clearcache() #很关键的一句，否则listbox调用时会刷新
    s = Filter(s,"--=(.*?)\n")
    return s

###从远程命令txt文件中中读取下发命令内容
def ReadCmdListWindowsDate(path,line):
    s = linecache.getline(path,line)
    linecache.clearcache()
    lineData=Filter(s,"=(.*?)\n")
    return  lineData

def SaveOnuCheckSN(data):
    path =os.getcwdu()
    ansDate = json.loads(data)
    onumac=ansDate['MAC']
    CheckSN = ansDate['CheckSN']
    OldData = linecache.getline("OnuList\List\\"+onumac+".ini",1)
    linecache.clearcache() #很关键的一句，否则listbox调用时会刷新
    OldData = Filter(OldData,"--=(.*?)\n")
    NewData = json.loads(OldData)
    NewData['CheckSN'] = CheckSN
    NewData = '----='+json.dumps(NewData)
    f = open(path+'\OnuList\List\\'+onumac+'.ini',"w+")
    f.write(NewData)
    f.close()
    print u"从RegisterFirst中获取到的CheckSN写入成功",NewData

def SaveOnuDevRND(data):
    path =os.getcwdu()
    ansDate = json.loads(data)
    onumac=ansDate['MAC']
    DevRND= ansDate['DevRND']
    OldData = linecache.getline("OnuList\List\\"+onumac+".ini",1)
    linecache.clearcache() #很关键的一句，否则listbox调用时会刷新
    OldData = Filter(OldData,"--=(.*?)\n")
    NewData = json.loads(OldData)
    NewData['DevRND'] = DevRND
    NewData = '----='+json.dumps(NewData)
    f = open(path+'\OnuList\List\\'+onumac+'.ini',"w+")
    f.write(NewData)
    f.close()
    print u"从Register中获取到的DevRND写入成功",NewData

"""
def ReadCmdListWindows(path):
    cmd = open(path,'r')
    cmddata=cmd.read()
    cmd.close()
    return  cmddata
"""
"""
def ReadCmdListWindowsDate(path,line):
    s = linecache.getline(path,line)
    linecache.clearcache()
    lineData=Filter(s,"=(.*?)\n")
    return  lineData

def Send_StrToJson(str_line):       ###listUp框中显示内容
    cmd=ReadConfigLineData(str_line).replace("{","\n\t{").replace(",",",\n\t")  #发送的命令添加换行Tab
    s = linecache.getline("config.ini",1)
    lineDemo=Filter(s,"=(.*?)\n")
    lineDemo = lineDemo.replace(",",",\n").replace("\"}","\n\"}") #########模版命令添加换行
    lineDemo = lineDemo.replace("CMD" , cmd, 1)
    return lineDemo



def Revce_StrToJson(str_rec):       ###listDown中返回数据显示
    Rev_dat=re.sub(":\s\"(.*?)\"\s", ":\"CMD\"", str_rec)    #使用正则表达获取返回demo
    print str_rec
    print Rev_dat
    Rev_cmd=OutouCommond(str_rec).replace("{","\n\t{").replace(",",",\n\t") #命令行修改格式
    Rev_dat=Rev_dat.replace(",",",\n").replace("\"}","\n\"}")               ##返回demo修改格式

    Rev=Rev_dat.replace("CMD" ,Rev_cmd, 1)                                    ##将命令添加到demo中返回显示
    return Rev

def Serche_Config(str):
    ct = 0
    list = []
    count = ReadConfigLineCount()
    while ct < count:
        s = linecache.getline("config.ini",ct)
        if Filter(s,str):
            list.append(ct)  ###减1和listbox对应
        ct+=1
    return list
    # print json.dumps(Response) ###   ###json 格式转换

def Delete_Tab():
    fr = open("config.ini","r")
    content = fr.readlines()
    fr.close()
    ct = 0
    print len(content)
    while ct<len(content):
        if content[ct]=="\n":
            del(content[ct])
        else:
            ct+=1
    print len(content)
    ct=0
    fw=open("config.ini","w")
    while ct <len(content):
        fw.write(content[ct])
        ct+=1
    fw.close()

def Add_Config_Cmd(Name,Cmd):
    fr = open("config.ini","r")
    content = fr.readlines()
    fr.close()   #repr
    print u"新增命令名",isinstance(Name, unicode)
    if isinstance(Name, unicode) == "True":
        content.insert(len(content),"\n-")
        content.insert(Name.encode("gbk"))
        content.insert("-="+Cmd)
    else:
        content.insert(len(content),"\n-"+Name+"-="+Cmd)
    ct=0
    fw=open("config.ini","w")
    while ct <len(content):
        fw.write(content[ct])
        ct+=1
    fw.close()"""