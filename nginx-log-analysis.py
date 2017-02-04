#! /usr/bin/env python
# coding:utf8
''' 从日志中汇总出 流量最大的前十个IP地址, 它的总流量,它访问最多的服务器资源、及流量'''
import sys
import os
from prettytable import PrettyTable


KB = 1024           #KB -> B  B是字节
MB = 1048576        #MB -> B  1024 * 1024
GB = 1073741824     #GB -> B  1024 * 1024 * 1024
TB = 1099511627776  #TB -> B  1024 * 1024 * 1024 * 1024




logDict = {}
countlist = []
datalist = []
with open(sys.argv[1])as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split() #通过split()函数,将每一行数据以空格为分隔符存成一个列表。
        ip = split_line[0]#通过位置下标将需要的值取出来如[0],[6],[9]等
        resourcePathName = split_line[6]
        resourceName = os.path.basename(resourcePathName)
        #通过os.path.basename,、
        # 将本来是:'/%E5%AE%89%E5%8D%93%E7%89%88%E6%9C%AC/%E5%AD%A6%E7%94%9F%E7%89%88/com.boxfish.stu-aiqiyi-release-v4.3.2-330.apk'\
        #只取它的文件名部份,将路径去掉。
        size = int(split_line[9])
        key_counts = 'counts'
        key_data = 'data'
        key_resources = 'resources'
        if ip not in logDict:
            logDict.setdefault(ip, {})[key_counts] = 1
            logDict.setdefault(ip, {})[key_data] = size
            logDict.setdefault(ip,{})[key_resources]={}
            temp = logDict[ip]
            temp.setdefault(key_resources, {})[resourceName] = size
        else:
            temp =logDict[ip]
            if resourceName in temp[key_resources].keys():
                temp[key_resources][resourceName] += size
            else:
                temp.setdefault(key_resources, {})[resourceName] = size
            logDict.setdefault(ip, {})[key_counts] += 1
            logDict.setdefault(ip, {})[key_data] += size
    for ip in logDict:
        countlist.append(logDict[ip][key_counts])
        datalist.append(logDict[ip][key_data])
top10_count = sorted(set(countlist),reverse=True)[:10]
top10_data = sorted(set(datalist), reverse=True)[:10]
# 下面求最多访问的资源:

rdict = {}
for i in logDict.keys():
    for rname in logDict[i][key_resources].keys():
        if rname not in rdict:
            rdict[rname] = logDict[i][key_resources][rname]
        else:
            rdict[rname] += logDict[i][key_resources][rname]
rsum = sorted(rdict.items(), key=lambda d: d[1], reverse=True)[:3]
print("服务器上被访问最多的资源是:")
print(rsum[0][0])
print("对该资源访问的总流量是: " + str(round(rsum[0][1]/GB,2)) + " GB" )
print()
print("流量前十的IP地址:从多到少")
#
table = PrettyTable(['IP地址','总流量','访问最多的服务器资源名','流量'])
for totalData in top10_data:
    for ipaddress in logDict.keys():
        if totalData == logDict[ipaddress][key_data]:
            max_resource = sorted(set(logDict[ipaddress][key_resources].values()),reverse=True)[0]
            for rname in logDict[ipaddress][key_resources].keys():
                if logDict[ipaddress][key_resources][rname] == max_resource:
                    if max_resource < KB:
                        table.align['IP地址'] = '1'
                        table.padding_width = 1
                        table.add_row([ipaddress,str(round(totalData/Bytes,2))+ " Bytes" ,rname,str(round(max_resource/Bytes,2))+ " Bytes" ])
                    elif KB <= max_resource < MB:
                        table.align['IP地址'] = '1'
                        table.padding_width = 1
                        table.add_row([ipaddress,str(round(totalData/KB,2))+ " KB" ,rname,str(round(max_resource/KB,2))+ " KB" ])
                    elif MB <= max_resource < GB:
                        table.align['IP地址'] = '1'
                        table.padding_width = 1
                        table.add_row([ipaddress,str(round(totalData/MB,2))+ " MB" ,rname,str(round(max_resource/MB,2))+ " MB" ])
                    elif GB <= max_resource < TB:
                        table.align['IP地址'] = '1'
                        table.padding_width = 1
                        table.add_row([ipaddress,str(round(totalData/GB,2))+ " GB" ,rname,str(round(max_resource/GB,2))+ " GB" ])
                    else:
                        table.align['IP地址'] = '1'
                        table.padding_width = 1
                        table.add_row([ipaddress,str(round(totalData/TB,2))+ " TB" ,rname,str(round(max_resource/TB,2))+ " TB" ])
print(table)



