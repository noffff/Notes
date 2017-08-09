# 工作机制
## 一个分片，单个索引的工作
每次接收新数据都会创建一个新的是实施所因。Lucene会把每次生成倒叙索引叫做 segment。每一次先将数据放入内存buffer，然后flush到磁盘，生成segment，索引指针commit会更新，指向该segment
后台会有进程将零散的segment归并为大的segment，提高性能。归并操作非常消耗磁盘IO和CPU。支持限速
```
curl -XPUT http://localhost:9200/_cluster/settings -d '
{
   "persistent" : { "indices.store.throttle.max_bytes_per_sec" : "100mb"}
}
'
5.0以后删除了该介绍，默认为10240MB
```
- 归并
  将多个小segment变为组合为大的segment
  - 归并线程 min(3,CPU核数/2)，这个值为默认的，还需要考虑磁盘性能
可以针对segment 的大小，一次归并数，归并segment的大小限制(大于多少不用归并)来设置。除此之外可以设置flush时间，这样刷到硬盘的segment就已经比较大，不过会相对来说占更多的内存
## Ela 层面
- 定位数据位置
  - 路由计算<br>
    每条数据都有routing参数，默认为id值。shard值=hash(id) % shard主分片数
    > 上述可看出shard主分片数不可更改，更改后shard会改变，数据将会找不到    
- 副本一致性
# 概念
- Shards & Replicas
  - 一个索引可能非常大，所以将一个索引可以分成很多片,将其存到不同的节点上，单个主机上的这个片或块的概念叫做Shard
  - 数据多副本，保证高可用 Replicas
- Document
  -  是一个可以索引的基础单元。
- Index
  - 一个索引就是一串有共同特征的字符集，用来搜索document。 
# 相关操作
> curl -X${Method} URL/index_name/type_name/id_number?pretty&pretty
- 导入历史数据，可以先关闭实时检索
```
curl -XPUT http://localhost:9200/index_name -d '
{
 "setting" :{ "refresh_interval" : "-1"}
}
'
```
- 恢复实时索引
```
curl -XPOST http://localhost:9200/index_name/_refresh
```

## 操作集群
- 检测集群index
`curl -XGET 'localhost:9200/_cat/indices?v&pretty'`
<br>
- 检测集群健康
  `curl -XGET 'localhost:9200/_cat/health?v&pretty'`
  - 集群健康状况会返回三种状态
    - Green 集群OK
    - Yello 集群数据没有副本,默认是一副本，所以单节点会报黄
    - Red   有些shard不可用
- 检测索引健康状况
  `curl -XGET 'localhost:9200/_cluster/health/test1,test2?pretty'`
- 检测集群节点列表
  `curl -XGET 'localhost:9200/_cat/nodes?v&pretty'`

## Index 
- 列出全部索引
  `curl -XGET 'localhost:9200/_cat/indices?v&pretty'`
- 自定义一个索引
  `curl -XPUT 'localhost:9200/Index_name?pretty&pretty'`
- 为一个索引添加 类型 数据。如果索引不存在会自动创建
```
PUT方法指定ID
curl -XPUT 'localhost:9200/Index_name/Type_name/ID_number?pretty&pretty' -H 'Content-Type: application/json' -d'
{
  "name": "John Doe"
}
'
POST方法不指定ID
curl -XPOST 'localhost:9200/customer/external?pretty&pretty' -H 'Content-Type: application/json' -d'
{
  "name": "Jane Doe"
}
- 查询shard层次的健康状况
```
curl -XGET 'localhost:9200/_cluster/health/shard?level=shards&pretty'
```
'
```
- 查询索引 类型的内容
```
curl -XGET 'localhost:9200/Index_name/Type_name/ID_number?pretty&pretty'
```
- 删除一个索引
```
curl -XDELETE 'localhost:9200/Index_name?pretty&pretty'
```
- 通过查询API删除
`curl -XPOST localhost:9200/index-name/_delete_by_query -d '{"query":{"match":{"field_name":"value"}}}'`
**e.g**:
```
curl -XPUT 'localhost:9200/customer?pretty'
curl -XPUT 'localhost:9200/customer/external/1?pretty' -H 'Content-Type: application/json' -d'
{
  "name": "John Doe"
}
'
curl -XGET 'localhost:9200/customer/external/1?pretty'
curl -XDELETE 'localhost:9200/customer?pretty'
```
- 关闭/打开索引索引。索引序号支持*
```
curl -XPOST 'localhost:9200/my_index/_close?pretty'
curl -XPOST 'localhost:9200/my_index/_open?pretty'
```
## Data
- 更新doc
  - 指定一个ID、索引、类型重复的执行PUT操作，会覆盖原有数据，@version字段+1。更新数据
  - 使用script更新值
- 删除doc
  `curl -XDELETE 'localhost:9200/index_num/type_num/ID?pretty&pretty'`
- bulk
  - ![批量操作](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/docs-bulk.html)
```
curl -XPOST 'localhost:9200/customer/external/1/_update?pretty&pretty' -H 'Content-Type: application/json' -d'
{
  "script" : "ctx._source.age += 5"
}
'
```

## 快照
- 注册快照仓库 
`curl -XPUT 'localhost:9200/_snapshot/仓库名' -H 'Content-Type: application/json' -d '{"type" : "fs","settings" : {"compress": true,"location":"/ES_backup/"} }'`
快照仓库的位置如果是绝对路径则必须在ES配置文件 path.repo中指定。如果是相对路径，则默认会在指定的路径中
- 创建快照
```
curl -XPUT 'localhost:9200/_snapshot/仓库名/快照名(必须小写)?pretty' -H 'Content-Type: application/json' -d'
{
  "indices": "index_1,index_2",
  "ignore_unavailable": true,
  "include_global_state": false
}
'
查询都有仓库都有哪些快照
curl -XGET 'localhost:9200/_snapshot/仓库名/*?pretty'   *也可以换成_all
```
- 完整的API手册
![API](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/cat.html)
