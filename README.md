# GrabIOCs Python 说明    
## 介绍   
支持`信誉值`和`类别过滤`的IOCs接口调用脚本

## 使用说明：
* config
    * 配置文件
    * 参数说明：
        * Appkey: 请求凭证
        * Appsecert: 请求凭证
        * Token: 订阅集合的Token值
        * SetName: 订阅集合名(可为空)
        * ScoreLevel: 数据类型为浮点型(必须带小数点)，信誉值下限默认默认为0.0
        * Useless: 数据类型为字符串数组，将不需要的类别填入即可    
        `IOCs类别:"spam", "scanner", "proxy", "c2", "phishing", "porn", "tor","gambling", "category", "dga", "trojan", "malware", "ransomware"`   
        `PS：其中"trojan","malware","ransomware"是没有信誉值的类（value值为hash值），进行判定时默认为0`
    * 配置示例：
    ```json
    {
        "Appkey":"xxxxxx",
        "Appsecert":"xxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "Token":"xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxx",
        "SetName":"test",
        "ScoreLevel":0.0,
        "Useless":["trojan","malware","ransomware"]
    }
    ```
* get-iocs.py
    * 逐页获取IOCs数据，保存在archive文件夹中
    * 支持断页续传,当从某页中断时，可将下页页码，作为参数，继续下载，最后获得的文件依旧完整
    * 一次IOCs数据同步约耗时40min

    * 使用示例：
    ```shell
    python get-iocs.py
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


    python get-iocs.py 134
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

