对多个日期索引的查询
例如 默认索引 logstash-*是基于日期做的索引
可以通过数学表达式替换索引的日期关键字查询<br>
`<索引字段的部分内容{日期表达式{日期格式|时区}}>`
- 日期表达式支持日期的增减操作
```
<logstash-{now/d{YYYY.MM.dd|+12:00}}>  十二小时以后
<logstash-{now/M-1M{YYYY.MM}}>        上个月
now/d会解析为当前日期
now/M解析为本月初
now/d为 2017年8月1日  进行日期处理来查询2016年8月
curl -XGET localhost:9200/%3Clogstash-%7Bnow%2FM-1y%2B24d%7D%3E/_search?pretty
```
ES默认返回的时区都是UTC时区。
在查询URL时相关字符串要变为urlcode
GET /<logstash-{now/d}>/_search => GET /%3Clogstash-%7Bnow%2Fd%7D%3E/_search
```
< %3C
> %3E
/ %2F
{ %7B 
} %7D
| %7C
+ %2B
: %3A
, %2C
```
将索引中的日期范围聚合查找
```
curl -XPOST 'localhost:9200/logstash*/_search?size=0&pretty' -H 'Content-Type: application/json' -d'
{
    "aggs": {
        "range": {
            "date_range": {
                "field": "date",
                "format": "MM-yyy",
                "ranges": [
                    { "to": "now-1y-5M/M" },从当前向前推1年5个月
                    { "from": "now/M" }
                ]
            }
        }
    }
}
'
```
- 查找字段的状态信息
  - 查找全部索引的字段
`curl -XGET 'localhost:9200/_field_stats?fields=*&pretty`
  - 查找指定索引字段
`curl -XGET 'localhost:9200/indx_name/_field_stats?fields=*&pretty`
  - 指定索引级别的字段查找
```
curl -XPOST 'localhost:9200/_field_stats?level=indices&pretty' -H 'Content-Type: application/json' -d'
{
   "fields" : ["field_name"]
}
'
```
- 包含以下几个项
  - 
## JSON格式的查询
- 简单查询，全文搜索
`curl -XGET localhost:9200/indexname/type/_search?q=search_content&commn_options`
- 字段搜索
`curl -XGET localhost:9200/indexname/type/_search?q=fields_name:search_content`
> 如果要对字段值进行精确查找，类似 grep -w 则在该值左右加上""
- 多检索条件
使用NOT、AND、OR组合
- 字段是否存在
  - _exists_:fields_name
  - _missing_:fields_name
- 范围搜索
  - date:["now-6h" TO "now"}  []符号表示包含该值类似于>= <=，{}不包含类似> <
- 近似搜索
  - "~"表示搜索单词可能有一两个字母不对

## 两种查询结构
- leaf query 
  类似于对某个特定值特定字段进行查询。关键字如 match、term、range
- Compound query
  组合复杂句的查询。


## 基于过滤内容的查询
- Query content
```
这个内容主要是定义，一个查询的范围内容。
这一块内容通过参数传递给search API
```
- Filter content
```
这块内容主要来选取上面得到的内容，通常这块常使用自带的字段内容。
```
- e.g
```
curl -XGET 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": { 
    "bool": { 
      "must": [
        { "match": { "title":   "Search"        }}, 
        { "match": { "content": "Elasticsearch" }}  
      ],
      "filter": [ 
        { "term":  { "status": "published" }}, 
        { "range": { "publish_date": { "gte": "2015-01-01" }}} 
      ]
    }
  }
}
'
```
