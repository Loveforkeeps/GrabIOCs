#!/usr/bin/python 
# -*- coding: utf-8 -*-
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant
import datetime
import json
import sys
import time
import io
import os
import csv
import importlib

# Python版本识别
if sys.version > '3':
    PY3 = True
else:
    PY3 = False
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print(u"---------------------当前环境为Python2,推荐使用Python3---------------------")

# 获取时间戳
timestamp1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp1)


# 获取系统日期
datestamp = time.strftime("%Y-%m-%d",time.localtime(time.time()))

# 获取脚本位置路径
path = os.path.split(os.path.realpath(__file__))[0] + '/'
os.chdir(path)

# 时间装饰器
def functime(func):
    def wap(*args,**kw):
       local_time = datetime.datetime.now()
       func(*args, **kw)
       times = (datetime.datetime.now() - local_time).seconds
       print('Run time is {} minutes {} seconds'.format(times//60,times%60))
    return wap

# 从config中获取参数
with io.open("config","r",encoding="utf8") as f:
    try:
        j = json.load(f)
        APPKEY = str(j["Appkey"])
        APPSECRET = str(j["Appsecert"])
        TOKEN = str(j["Token"])
        TYPE = ",".join(j["Type"])
        SCORELEVEL = j["ScoreLevel"]

        if len(APPKEY) and len(APPSECRET) and len(TOKEN):
            print("--- 从config文件中读取参数成功 ---")
            print(("IOCs类型:{}".format(TYPE)))
            print(("分值下限:{}".format(SCORELEVEL)))
        else:
            print("config文件中必要参数缺失！")
            exit(0)
    except:
        print("config文件中参数异常！")
        exit(0)

# 判断文件位置是否存在，若不存在则创建,用于存放下载下来的数据
domainpath = 'archive'
if not os.path.exists(domainpath):
    os.makedirs(domainpath)
    print((domainpath + ' has been created!'))

# 指定获取的页码
PAGENUM = ""
DATE = datestamp
if len(sys.argv) == 2:
    PAGENUM = sys.argv[1]
else:
    PAGENUM = "1"

# 设定存放iocs的csv文件名及相对路径
IOCS_CSVNAME = "archive/IOCS_"+DATE+".csv"

# 设置ALI云API请求参数
host = "https://api.tj-un.com"
url = "/v1/iocs"

cli = client.DefaultClient(app_key=APPKEY, app_secret=APPSECRET)
req_post = request.Request(host=host, protocol=constant.HTTPS, url=url, method="POST", time_out=120)

bodyMap={}
bodyMap["token"] = TOKEN
bodyMap["type"] = TYPE
bodyMap["score_from"] = SCORELEVEL
# bodyMap["limit"]
# bodyMap["qurey"] = "reports"




def json_csv(data,filename):
    """  将iocs的JSON数据转换为CSV """
    with io.open(filename,'a',encoding='utf-8') as f:
        header = ['category', 'score', 'geo', 'value', 'type', 'source_ref', 'tag', 'timestamp']
        dw = csv.DictWriter(f, header)
        if PAGENUM == "1":
            dw.writeheader()
        for row in data:
            row.update(row['reputation'][0])
            row.pop('reputation')
            dw.writerow(row)
    return 0

def json_csv_2(data,filename):
    """  将iocs的JSON数据转换为CSV """
    with io.open(filename,'ab') as f:
        header = [u'category', u'score', u'geo', u'value', u'type', u'source_ref', u'tag', u'timestamp']
        dw = csv.DictWriter(f, header)
        if PAGENUM == "1":
            dw.writeheader()
        for row in data:
            row.update(row['reputation'][0])
            row.pop('reputation')
            dw.writerow(row)
    return 0

def apires(page):
    bodyMap["page"] = page
    req_post.set_body(bodyMap)
    req_post.set_content_type(constant.CONTENT_TYPE_FORM)
    res = cli.execute(req_post)

    try:
        j=json.loads(res)
    except ValueError:
        if len(res):
            print(("Response: {}".format(res)))
        # print("Header: {}".format(res.header))
            print("API请求失败，请检查config参数")
            sys.exit(0)
        else:
            print("云端无响应")
        return 0
    except Exception as e:
        print(("获取数据异常:{}".format(e)))
        print(("Response: {}".format(res)))
        raise
        return 0
    if PY3:
        json_csv(j["response_data"][0]['labels'],IOCS_CSVNAME)
    else:
        json_csv_2(j["response_data"][0]['labels'],IOCS_CSVNAME)

    return j["nextpage"]
    
@functime
def main():
    retry = 50
    global PAGENUM
    print("--- 开始获取IOCs ---")
    try:
        nextpage = apires(PAGENUM)
        while nextpage and retry > 0:
            PAGENUM = nextpage
            print(("Next Page is {}".format(nextpage)))
            nextpage = apires(PAGENUM)
            if nextpage == 0:
                print("无响应，5秒后再次尝试")
                time.sleep(5)
                nextpage = PAGENUM
                retry = retry - 1
        else:
            if nextpage == "":
                print("That's All!")
            else:
                if retry == 0:
                    print("50重试耗尽，任务被迫结束")
                else:
                    print("如果重试多次仍出现这样的提示，请联系support@tj-un.com解决")
    except Exception as e:
        print(e)
        raise
        return 0
    except KeyboardInterrupt:
        print("\nUser Termined!")

if __name__ == '__main__':
    main()
