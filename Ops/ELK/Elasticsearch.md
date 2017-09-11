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
每个shard都是一个Lucene索引，一个Lucene索引的doc是有最大限制。其最大值为**2,147,483,519 (= Integer.MAX_VALUE - 128)**,可以通过_cat/shards API查询
---
## 相关参数设置
Elasticsearch是基于java，运用JVM  
### heap size
要对Elasticsearch的内存进行限制，就要通过限制JVM来设置  
JVM的初始化内存大小与最大heap size是不一致的，可能会因为JVM动态调整内存大小引起卡顿。 为了避免这个问题，要将JVM初始内存设为最大heap size一致。此外，如果"bootstrap.memory_lock"开启，那么JVM会在启动时将锁定初始化内存大小。 这个前提是初始化大小等于heap size大小，并且用户拥有"memlock unlimited"否则无效  
"bootstrap.memory_lock"该参数也防止数据交换到磁盘上，在JVM进行垃圾回收时防止磁盘颠簸  
检测是否开启内存锁
	'localhost:9200/_nodes?filter_path=**.mlockall&pretty'
[开启内存锁方法](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration-memory.html#mlockall)

### 文件描述符
Elasticsearch需要大量的文件描述符，因为每个shard都是有大量的段和其他文件组成  
因此要根据集群数据量来修改file descriptor的限制，超出文件描述符限制其结果可能会导致数据的丢失   
```
[关闭文件现在的方法](https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-system-settings.html)
节点最大文件限制
# curl -XGET 'localhost:9200/_nodes/stats/process?filter_path=**.max_file_descriptors&pretty'
```   
一般需要将Elasticsearch文件描述符限制提到65536或者更高  

### 最大线程
Elasticsearch执行请求操作时将请求分成多个阶段，然后将这些阶段放入不同的线程池进行处理  
Elasticsearch中有多种线程池。Elasticsearch需要能够创建许多进程，最大线程数是为了保证Elasticsearch能够创建足够多的线程用来使用。  
最大线程数的限制只在Linux中有，至少要允许创建2048个线程  
设置方法
	/etc/security/limits.conf nproc

### 设置垃圾收集器
JDK的JVM有很多种垃圾收集器，"serial collector"适合用于单核CPU的机器或者较小的heap。  
如果使用这个，对Elasticsearch可以说是毁灭性的。不能用它，默认使用CMS 收集器  
---
## 使用方法
### 优化
- 防止索引冲突
`elasticsearch.yml`
	rest.action.multi.allow_explicit_index: false
- Flat 输出
```
# curl -XGET 'localhost:9200/index_name/_settings?flat_settings=true&pretty'
输出如下
{
  "twitter" : {
    "settings": {
      "index.number_of_replicas": "1",
      "index.number_of_shards": "1",
      "index.creation_date": "1474389951325",
      "index.uuid": "n6gzFZTgS664GUfx0Xrpjw",
      "index.version.created": ...,
      "index.provided_name" : "twitter"
    }
  }
}
```

### Indices操作
#### 创建索引
##### 设定索引属性
每个索引都有自己的特性，如果需要全局可以设置Template属性  
- 指定索引属性
```
curl -XPUT 'localhost:9200/index_name?pretty' -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "index" : {
            "number_of_shards" : 3,     # 默认5
            "number_of_replicas" : 2    # 默认1
        }
    }
}
'
```
[更多详细参数](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html)

##### Template
创建模板，将创建的索引按照模板进行设置  
模板包含两部分
- 简单的匹配Template的部分，决定索引是否用该模板  
- settings
- mappings
[详细内容](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html)
##### 设定映射 Mapping
映射是定义一个doc的字段存储什么样的内容，并且如何被索引的过程。  
定义的内容如下  
- 哪些字符字段应该被视为全文字段
- 哪些字段包含数字、日期、地理位置
- doc中的所有字段的值是否应该被`_all`字段索引
- 日期的格式
- 自定义规则来控制动态的添加字段

```
[详细内容](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping)
curl -XPUT 'localhost:9200/test?pretty' -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings" : {
        "type1" : {
            "properties" : {
                "field1" : { "type" : "text" }
            }
        }
    }
}
'
```
##### 检查索引是否存在
	curl -I 'localhost:9200/index_name?pretty'

### doc操作
有时候有些数据没有被刷到disk上，会存在translate.log里也不会丢失  
但是如果想立刻生效写入磁盘可以使用
	curl -XPOST 'localhost:9200/index_name/_flush/synced?pretty'
但是如果想立刻建立lucene索引使其可以被搜索可以使用  
	curl -XPOST 'localhost:9200/index_name/_refresh?pretty'
以上俩种都有固定周期限制
#### 创建doc
```
# curl -XPUT 'localhost:9200/index_name/type_name/ID?pretty&pretty' -H 'Content-Type: application/json' -d'
{
  "Key": "Value"
}
'
```
#### 查询doc
cat API能查看集群多个状态  
使用下列方式能列出所有可执行API
	curl -XGET 'localhost:9200/_cat?&pretty'
两种查询方式  
一种将参数直接通过URL传入  
一种通过请求body传入
##### 简单查询
- 正常查询
	# curl -XGET 'localhost:9200/index_name/type_name/ID?pretty&pretty'
- search
	curl -XGET 'localhost:9200/index_name/_search?q=*&sort=account_number:asc&pretty&pretty'
	q=*参数匹配索引中的所有，sort=account_number:asc参数表示使用account_number字段的值升序排序
	q=key:value参数匹配索引中的所有
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
# curl -XGET 'localhost:9200/index_name/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} }
}
'
# curl xxx
{
  "query": { "match_all": {} },
  "_source": ["account_number", "balance"]
}

# curl xxx
{
  "query": { "match": { "Key": "value1 value2" } }
}

# curl xxx
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
# curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
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
# curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
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
# curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
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
# curl -XGET 'localhost:9200/bank/_search?pretty' -H 'Content-Type: application/json' -d'
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
##### 通过查询删除
查询删除时，会返回删除的一个结果也就是快照的东西。并删除真正的数据  
得到的这个快照就是version conflict。这个数就是通过查询删除的数量  
在查询删除期间，会有大量的搜索请求按顺序的查找所有匹配的doc来删除。 
每次找到一批doc，就会有与之对应的一批用来删除的bulk请求。  
一个搜索请求或bulk请求被拒绝，依照默认策略充实 10次，如果还失败就返回错误  
- 简单查询删除

- JSON方式的复杂查询删除
```
# curl -XPOST 'localhost:9200/index_name/_delete_by_query?pretty' -H 'Content-Type: application/json' -d'
{
  "query": { 
    "match": {
      "message": "some message"
    }
  }
}
'
```
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
## 集群操作
集群中有多个节点组成  
集群等级的操作大部分都可以通过指定节点来对节点操作  
可以指定如"_local"或者节点地址、节点名  
请求时可以带参数  
- level
默认cluster，可以指定indices、shards
- wait_for_status
等待状态的改变，默认不等待
- wait_for_no_relocating_shards
是否等待集群没有shard的重新分配。默认false
- wait_for_active_shards
数字单位，指定等待多少个shards变为active。`all`是等待集群中所有shards变为active，默认为`0`
- wait_for_nodes
这个请求会等待有多少个节点变为可用状态。接收条件语句如 >=Number或者ge(Number)等
- timeout
时间参数，控制超时的时间
- local
布尔值，如果为true返回本地信息

### 集群健康状态检测
```
集群状态
# curl -XGET 'localhost:9200/_cluster/health?pretty'

索引状态
# curl -XGET 'localhost:9200/_cluster/health/index1,index2?pretty'
```  

### 集群状态
集群的全部信息
```
curl -XGET 'http://localhost:9200/_cluster/state'

对信息进行过滤  
curl -XGET 'http://localhost:9200/_cluster/state/{metrics}/{indices}'
```

#### metrics
- version
集群的状态版本
- master_node
响应的master_node
- nodes
响应的节点
- routing_table
响应的`routing_table`,也就是shard
- blocks
响应的`blocks`

### 集群数据统计
反应集群层次的相关数据如 shard数、store size、memory usage以及当前节点的相关信息  
	curl -XGET 'http://localhost:9200/_cluster/stats?human&pretty'

### 集群任务
#### 任务管理
查询当前任务
```
集群中所有任务
curl -XGET 'localhost:9200/_tasks?pretty'
指定节点上的任务
curl -XGET 'localhost:9200/_tasks?nodes=nodeId1,nodeId2&pretty'
指定节点上的与集群相关的任务
curl -XGET 'localhost:9200/_tasks?nodes=nodeId1,nodeId2&actions=cluster:*&pretty'
通过任务ID查询任务
curl -XGET 'localhost:9200/_tasks/task_id:1?pretty'
curl -XGET 'localhost:9200/_tasks?parent_task_id=parentTaskId:1&pretty'
```  
查看任务列表
```
curl -XGET 'localhost:9200/_cat/tasks?pretty'
curl -XGET 'localhost:9200/_cat/tasks?detailed&pretty'
```  
取消任务
	curl -XPOST 'localhost:9200/_tasks/node_id:task_id/_cancel?pretty'
	curl -XPOST 'localhost:9200/_tasks/_cancel?nodes=nodeId1,nodeId2&actions=*reindex&pretty'


#### 集群中等待任务
查询集群层次的将要进行的改变,如创建索引、升级mapping、分配shard等这些还没有被执行的操作  
	curl -XGET 'http://localhost:9200/_cluster/pending_tasks'
执行上述命令，一般返回结果都会为空，因为改变发生的比较快。 

### 集群路由调整
该功能能够对集群内部的路由进行调整，比如 将一个shard从一个节点调到另一个节点，也可以取消分配等  
#### 参数
##### commands 参数
- move
将一个shard从一个节点移到另一个，接收指定的编号的shard和索引  
- cancel
取消或恢复一个shard的分配操作，`node`参数指定取消哪一个节点上的shard分配。  
也支持使用`allow_primary`标志，标记允许主shard的分配。
- allocate_replica
分配一个未备分配的replica shard给一个节点。接收`index`和`shard`参数指定的索引名和shard号  `node`参数指定节点
集群会尝试分配shard，直到失败次数达到`index.allocation.max_retries`默认为5.  
在这之后可以用`reroute`来进行再次分配
例子  
```
curl -XPOST 'localhost:9200/_cluster/reroute?pretty' -H 'Content-Type: application/json' -d'
{
    "commands" : [
        {
            "move" : {
                "index" : "test", "shard" : 0,
                "from_node" : "node1", "to_node" : "node2"
            }
        },
        {
          "allocate_replica" : {
                "index" : "test", "shard" : 1,
                "node" : "node3"
          }
        }
    ]
}
'
```
> 当一个shard从A节点移动到另一个B，那么B节点上原来的shard会移动到A节点。集群特性。这种情况可以关闭集群的 allocations功能  

 
