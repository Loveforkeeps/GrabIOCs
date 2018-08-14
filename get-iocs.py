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

# 获取时间戳
timestamp1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp1)
reload(sys)
sys.setdefaultencoding('utf-8')

# 获取系统日期
datestamp = time.strftime("%Y-%m-%d",time.localtime(time.time()))

# 获取脚本位置路径
path = os.path.split(os.path.realpath(__file__))[0] + '/'
os.chdir(path)

# 从config中获取参数

with io.open("config","r",encoding="utf8") as f:
    try:
        j = json.load(f)
        APPKEY = str(j[u"Appkey"])
        APPSECRET = str(j[u"Appsecert"])
        TOKEN = str(j[u"Token"])
        TYPE = ",".join(j[u"Type"])
        # USELESS = j[u"Useless"]  #需要去除的iocs类别队列
        # SCORELEVEL = j[u"ScoreLevel"]
        if len(APPKEY) and len(APPSECRET) and len(TOKEN):
            print(u"从config文件中读取参数成功")
        else:
            print(u"config文件中必要参数缺失！")
            exit(0)
    except:
        print(u"config文件中参数异常！")
        exit(0)

    


# 判断文件位置是否存在，若不存在则创建,用于存放下载下来的数据
domainpath = 'archive'
if not os.path.exists(domainpath):
    os.makedirs(domainpath)
    print(domainpath + ' has been created!')

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

def main():
    global PAGENUM
    bodyMap["token"] = TOKEN
    bodyMap["page"] = PAGENUM
    bodyMap["type"] = TYPE
    # bodyMap["limit"]
    # bodyMap["qurey"] = "reports"
    # bodyMap["score_from"] = SCORELEVEL
    
    req_post.set_body(bodyMap)
    req_post.set_content_type(constant.CONTENT_TYPE_FORM)
    res = cli.execute(req_post)
    # with open(PAGENUM+".json","w") as f:
    #     f.write(res)
    try:
        j=json.loads(res)
    except ValueError:
        if len(res):
            print("Response: {}".format(res))
        # print("Header: {}".format(res.header))
            print(u"API请求失败，请检查config参数")
        else:
            print("Response: {}".format(res))
            print(u"无返回结果，再次尝试")
            main()
        return 0
    except Exception as e:
        print("Response: {}".format(res))
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
    except Exception as e:
        with open("erro.log","w") as f:
            f.write(res)
        print(e)
        return 0


# 将iocs的JSON数据转换为CSV
def json_csv(data,filename):
    # global SCORELEVEL
    with open(filename, 'a') as f:
        dw = csv.DictWriter(f, [u'category', u'score', u'geo', u'value', u'geo', u'type', u'source_ref', u'tag', u'timestamp'])
        if PAGENUM == "1":
            dw.writeheader()
        # dw.writeheader()
        for row in data:
            # print(row)
            row.update(row['reputation'][0])
            row.pop('reputation')
            # print(row)
            dw.writerow(row)
            # if row['category'] not in USELESS :          # 排除部分IOC类别
            #     if float(row.get('score',0.1)) > SCORELEVEL:    # 信誉值过滤
            #         dw.writerow(row)
            # # 去除过长的value
            # if row['category'] not in useless and len(row['value']) < 45:
            #     dw.writerow(row)
    return 0

if __name__ == '__main__':
    main()
    # 获取时间戳
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(timestamp)
