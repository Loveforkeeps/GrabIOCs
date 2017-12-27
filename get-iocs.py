#!/usr/bin/python 
# -*- coding: utf-8 -*-
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant
import json
import sys
import time
import io
import os
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

# 获取系统日期
datestamp = time.strftime("%Y-%m-%d",time.localtime(time.time()))

# 获取脚本位置路径
path = os.path.split(os.path.realpath(__file__))[0] + '/'
os.chdir(path)

# 从config中获取参数

with io.open("config","r",encoding="utf8") as f:
    j = json.load(f)
    APPKEY = str(j[u"Appkey"])
    APPSECRET = str(j[u"Appsecert"])
    TOKEN = str(j[u"Token"])
    USELESS = j[u"Useless"]  #需要去除的iocs类别队列
    SCORELEVEL = j[u"ScoreLevel"]
    
    if len(APPKEY) and len(APPSECRET) and len(TOKEN):
        print(u"从config文件中读取参数成功")
    else:
        print(u"config文件中必要参数缺失！")
        exit(0)

# 判断文件位置是否存在，若不存在则创建,用于存放下载下来的数据
domainpath = 'archive'
if not os.path.exists(domainpath):
    os.makedirs(domainpath)
    print(domainpath + ' has been created!')

# 设定存放iocs的csv文件名及相对路径
IOCS_CSVNAME = "archive/IOCS_"+datestamp+".csv"

# 指定获取的页数，日期（默认为执行时间）
PAGENUM = ""
if len(sys.argv) == 2:
    PAGENUM = sys.argv[1]
else:
    PAGENUM = "1"
DATE = time.strftime("%Y-%m-%d",time.localtime(time.time()))

# 设置ALI云API请求参数
host = "https://apiiocs.sec-un.com"
url = "/v1/iocs"

cli = client.DefaultClient(app_key=APPKEY, app_secret=APPSECRET)
req_post = request.Request(host=host, protocol=constant.HTTPS, url=url, method="POST", time_out=120)

bodyMap={}

def main():
    global PAGENUM
    bodyMap["token"] = TOKEN
    bodyMap["date"] = DATE
    bodyMap["page"] = PAGENUM
    # bodyMap["type"] = "indicator"
    # bodyMap["qurey"] = "reports"
    
    
    req_post.set_body(bodyMap)
    req_post.set_content_type(constant.CONTENT_TYPE_FORM)
    res = cli.execute(req_post)

    try:
        j=json.loads(res)
    except ValueError:
        print(res)
        print(u"API请求失败，请检查config参数")
        return 0
    except Exception as e:
        print(res)
        raise
        return 0

    
    # print(len(j["response_data"][0]['labels']))

    json_csv(j["response_data"][0]['labels'],IOCS_CSVNAME)

    try:
        nextpage = j["nextpage"]

        if not nextpage == "":
            PAGENUM = nextpage
            print(u"Next Page is "+nextpage)
            main()
        else:
            print(u"That's All!")
    except:
        print(j)
        return 0


# 将iocs的JSON数据转换为CSV
def json_csv(data,filename):
    global SCORELEVEL
    with open(filename, 'a') as f:
        dw = csv.DictWriter(f, [u'category', u'geo', u'value', u'score', u'created_time', u'type', u'source_ref'])
        if PAGENUM == "1":
            dw.writeheader()
        # dw.writeheader()
       
        for row in data:
            row['category'] = row['category'][0]
            
            if row['category'] not in USELESS:          # 排除部分IOC类别
                if float(row.get('score',0.1)) > SCORELEVEL:    # 信誉值过滤
                    dw.writerow(row)
                        
            # # 去除过长的value
            # if row['category'] not in useless and len(row['value']) < 45:
            #     dw.writerow(row)

if __name__ == '__main__':
    main()
