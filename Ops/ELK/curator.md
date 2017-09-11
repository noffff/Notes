高复杂性的操作
入口配置文件，一般默认为`~/.curator/curator.yml`

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
