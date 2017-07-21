# 概念
- Shards & Replicas
  - 一个索引可能非常大，所以将一个索引可以分成很多片,将其存到不同的节点上，这个功能叫做Shard
  - 数据多副本，保证高可用 Replicas
  - 一个Document是一个可以索引的基础单元。
# 相关操作
- 检测集群index
`curl -XGET 'localhost:9200/_cat/indices?v&pretty'`
- 检测集群是否健康
  - `curl -XGET 'localhost:9200/_cat/health?v&pretty'`
  - 集群健康状况会返回三种状态
    - Green 集群OK
    - Yello 集群有些没有分配的副本
    - Red   有些数据不可用
- 完整的API手册
![API](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/cat.html)
