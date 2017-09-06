## 概念
### 集群
一至多个节点共同处理整个数据并提供跨节点的查询、定位索引能力。  
一个节点只能属于一个集群，每个集群都有独立的名字。默认为elasticsearch  
### 节点
集群的一部分，用来存储部分/完整的数据。为集群提供索引及查询能力。  
初始化节点时会默认分片随机的识别名称(UUID)，也可以自己定义名称  
节点可以自动初始化一个默认名为"elasticsearch"。
### 索引
一个索引是一个doc的集合。索引的名称必须是小写，在索引、查询、升级以及删除操作doc时会用到  
### document
doc是索引一条信息的基本单元。其格式为JSON
### Shards
一条索引可以存储大量的数据。当索引存在于单一节点时，会有明显的性能限制，对这个单一节点进行查询操作会非常慢  
为了解决这个问题，Elasticsearch支持将一个索引分割为大量分片,这些分片就是shard。  
每个shard都具有完整的功能及被索引功能,这样就可以将这些shard存放于集群中的任一节点  
- shard这种机制使管理员能够水平调整一个节点的数据大小
- 允许将操作如查询等在多个shard中同时进行，能够提高性能和吞吐量  
shard的分布以及将一个扩散到多个shard的查询请求整合返回的操作是在Elasticsearch内部完成，对于用户来说是完全透明的  
### Replicas
为了防止错误减少故障率,提高可用性，Elasticsearch支持对索引的shard创建副本，这种叫做replica shard  
- Replica提供了shard/node的高可用性，所以相同的replica node是不能分配到相同节点。
- 可以将搜索等请求直接放在replica中，提高吞吐量
每个索引可以划分为多个shards。一个索引可以有0到多个副本，一旦创建了副本就有primary shard和replica shard  
shards和replica的数量可以在索引被建立前定义，在索引创建后，可以动态改变replica的值，但是不能改变已经生效的shards  

每个shard都是一个Lucene索引，一个Lucene索引的doc是有最大限制。其最大值为**2,147,483,519 (= Integer.MAX_VALUE - 128) **,可以通过_cat/shards API查询
## 相关参数设置
Elasticsearch是基于java，运用JVM  
要对Elasticsearch的内存进行限制，就要通过限制JVM来设置  
JVM的初始化内存大小与最大heap size是不一致的，可能会因为JVM动态调整内存大小引起卡顿。 为了避免这个问题，要将JVM初始内存设为最大heap size一致。此外，如果"bootstrap.memory_lock"开启，那么JVM会在启动时将锁定初始化内存大小。 这个前提是初始化大小等于heap size大小，否则无效  
## 使用方法
### doc操作
#### 创建doc
```
# curl -XPUT 'localhost:9200/index_name/type_name/ID?pretty&pretty' -H 'Content-Type: application/json' -d'
{
  "Key": "Value"
}
'
```
#### 查询doc
两种查询方式  
一种将参数直接通过URL传入  
一种通过请求body传入
##### 简单查询
- 正常查询
	# curl -XGET 'localhost:9200/index_name/type_name/ID?pretty&pretty'
- search
	curl -XGET 'localhost:9200/index_name/_search?q=*&sort=account_number:asc&pretty&pretty'
	q=*参数匹配索引中的所有，sort=account_number:asc参数表示使用account_number字段的值升序排序
  - 返回结果字段解释
    - took
花费的时间
    - timed_out
是否超时
    - _shards
查询了几个shard中，并且成功和失败的数量
    - hits
查询结果
    - hits.total
多少doc匹配
    - hits.hits
查询结果，默认前10个doc
    - hits.sort
查询结果使用的排序key
    - hits._score max_score
忽略这些字段
##### 复杂查询
JSON格式的查询，类似于DSL  
###### match query
```
curl -XGET 'localhost:9200/index_name/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} }
}
'
curl xxx
{
  "query": { "match_all": {} },
  "_source": ["account_number", "balance"]
}

curl xxx
{
  "query": { "match": { "Key": "value1 value2" } }
}

curl xxx
{
  "query": { "match_phrase": { "address": "mill lane" } }
}
```  
- query
表明查询的方式
  - match_all
该种类型的查询时查询指定索引中的全部doc  
  - _source
只查看这些doc中的这些资源
  - match
key字段包含value1或value2的
  - match_phrase
address包含 "mill lane"的doc
###### bool query
能够将多个小的查询组合成较大的查询
```
must 查询两个必须都为true
address字段必须包含 "mill"和"lane"
curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}
'
should 查询列表中满足一个即可
curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "should": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}
'
must_not 查询列表必须都不是true
curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must_not": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}
'
```  
限定词 must、should等还可以组合使用  
```
curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "age": "40" } }
      ],
      "must_not": [
        { "match": { "state": "ID" } }
      ]
    }
  }
}
'
```
##### filter
该方法能够对查询的结果进行过滤  
#### 删除doc
	将GET方法换位DELETE方法即可
#### 修改doc内容
```
# curl -XPOST 'localhost:9200/index_name/type_name/ID/_update?pretty&pretty' -H 'Content-Type: application/json' -d'
{
  "doc": { "Key": "Value" }
}
'
```
#### 批量操作
批量中的一个操作失败，不会影响其他操作  
```
# curl -XPOST 'localhost:9200/index_name/type_name/_bulk?pretty&pretty' -H 'Content-Type: application/json' -d'
{"index":{"_id":"1"}}
{"name": "John Doe" }
{"index":{"_id":"2"}}
{"name": "Jane Doe" }
'
# curl -XPOST 'localhost:9200/index_name/type_name/_bulk?pretty&pretty' -H 'Content-Type: application/json' -d'
{"update":{"_id":"1"}}
{"doc": { "name": "John Doe becomes Jane Doe" } }
{"delete":{"_id":"2"}}
'
```

