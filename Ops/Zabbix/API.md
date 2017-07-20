- API接口：api_jsonrpc.php
- HTTP header：Content-Type: application/json-rpc|"Content-Type":"application/json"
- POST数据必须要JSON格式
- Python3 POST例子,登录Zabbix
```
import urllib3
import json

Zabbix_Cusor = urllib3.PoolManager()
Zabbix_url = "http://10.211.55.3/zabbix/api_jsonrpc.php"
Zabbix_username = 'Admin'
Zabbix_pass = 'zabbix'
Zabbix_header = {"Content-Type":"application/json"}

login_data = json.dumps(
    {"jsonrpc" : "2.0",
     "method" : "user.login",
     "params" :
         {
             "user" : "Admin",
             "password" : "zabbix",
             "userData" : "false",
         },
     "id" : 0
     }).encode('utf-8')
a  = Zabbix_Cusor.request('POST',
                          Zabbix_url,
                          body=login_data,
                          headers=Zabbix_header)
```

