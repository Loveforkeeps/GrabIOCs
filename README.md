#  RedQueen API2.0 Python 说明    
## 介绍   
天际有盟 RedQueen API2.0 Python接口请求工具，支持Python2/3。

**Attention：** 本工具非官方版本，仅供参考。

## 使用说明：
* config
    * 配置文件
    * 参数说明：
        * Appkey: 请求凭证
        * Appsecert: 请求凭证
        * Token: 订阅集合的Token值
        * Type：制定需要获取的IOC类型
          * 可选类型：feed_ipv4,feed_domain,feed_url,feed_hash-md5,feed_hash-sha1,feed_hash-sha256,feed_email 
        * SetName: 订阅集合名(可为空)
        * ScoreLevel：信誉值下限
    * 配置示例：
    ```json
    {
        "Appkey":"xxxxxx",
        "Appsecert":"xxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "Token":"xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxx",
        "Type":["feed_url","feed_ipv4"],
        "SetName":"test",
        "ScoreLevel":""
    }
    ```

* get-iocs.py
    * 逐页获取IOCs数据，保存在archive文件夹中
    * 支持断页续传,当从某页中断时，可将下页页码，作为参数，继续下载，最后获得的文件依旧完整
    * 一次IOCs数据同步约耗时40min
* 使用示例：
    
```shell
    $ python  get-iocs.py -h
    usage: get-iocs.py [-h] [-c CONFIG] [-ssf SSF]
    
    IOCs to CSV
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Specify the config file.
      -ssf SSF              Strict score filter.  （严格分数过滤，不保存没达到分数的同值关联IOC）
    ```
    
    
    
    ```shell
$ python get-iocs.py
    输出：
    从config文件中读取参数成功
    Next Page is 2
    Next Page is 3
    Next Page is 4
    Next Page is 5
    ...
    ...
    Next Page is 210
    Next Page is 211
    Next Page is 212
    That's All!
    ```
    
    ```shell
    # 断页续传
    $ python get-iocs.py 134
    输出：
    从config文件中读取参数成功
    Next Page is 134
    Next Page is 135
    ...
    ...
    Next Page is 210
    Next Page is 211
    Next Page is 212
    That's All!
    
    ```
    
    ```shell
    # 严格分数过滤，不保存没达到分数的同值关联IOC
    $ python get-iocs.py -ssf true
    ```
    
    

#### ToDo:

2019-04-26: 修改com.aliyun.api.gateway.sdk.client.DefaultClient.execute()，增加状态码检测，获取Header中的错误信息返回

