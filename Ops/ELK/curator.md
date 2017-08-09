高复杂性的操作
入口配置文件，一般默认为`~/.curator/curator.yml`
- 例子
```
---
# Remember, leave a key empty if there is no value.  None will be a string,
# not a Python "NoneType"
client:
  hosts:
    - 127.0.0.1
  port: 9200
  url_prefix:
  use_ssl: False
  certificate:
  client_cert:
  client_key:
  ssl_no_validate: False
  http_auth:
  timeout: 30
  master_only: False

logging:
  loglevel: INFO
  logfile:
  logformat: default
  blacklist: ['elasticsearch', 'urllib3']
```

动作定义:
- 动作文件
  该文件root字段必须为**actions**,然后是动作的需要 1.2.3.....Action是按照这个序号执行。
- 动作一般包含有以下元素
  - action
  - description
  - options
  - filters
指定filter时要先有**filtertype**，一共有几种类型的(filtertype)[https://www.elastic.co/guide/en/elasticsearch/client/curator/current/filtertype.html]
- 动作都包括
  - Alias
  - Allocation
  - Close
  - Cluster Routing
  - Create Index
  - Delete Indices
  - Delete Snapshots
  - Forcemerge
  - Index Settings
  - Open
  - Reindex
  - Replicas
  - Restore
  - Rollover
  - Snapshot
> 针对不同动作有不同的option，具体查看官网
