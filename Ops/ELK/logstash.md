> Logstsh实现的功能就类似 cat xxx|awk xxx|tee xxx(除此外还支持解码，编码)。cat就类似Logstash中的输入，awk类似filter，tee类似输出
## Logstash工作方式
- Input
- Filter
  - grok 分析事件，将文本格式化
  - mutate 对事件进行操作，增删改查
  - drop  丢弃事件
  - clone 对事件进行复制
  - geoip 将IP加上地理信息 
- Output
- Codec
  - json
  - multline
    多行的what参数 next代表 不匹配的行会从组合到下一行，previous组合到上一行
> Logstash每一个input都是一个java线程，对于事件的处理都在内存中进行，如果怕数据不安全丢失，可以在硬盘上处理
logstash使用file做input时有自己的文件记录上次传输到哪里。所以如果不想启用该功能则将其定位到/dev/null
```
sincedb_path => "/dev/null"
```
### 简单的教程
- 从终端标准输入获得输入，将输出定向到标准输出
```
logstash -e 'input{stdin{}}output{stdout{codec=>rubydebug}}'
输入 hello world 会输出
{
    "@timestamp" => 2017-07-23T13:06:41.003Z,
      "@version" => "1",
          "host" => "vm1",
       "message" => "hello world"
}
```
由此可看出Logstash其实由inpiut和output组成，中间会包含filter<br>
可以选择不同的input和output插件，支持多选。比如将上述内容也输出到Elasticsearch中<br>
可以写为
```
input {
     stdin{}
}
output{
     stdout {
            codec=>rubydebug
      }
     elasticsearch {
         host=>["127.0.0.1:9200"]
      }
}
```
### Logstash的线程
   - >xx输出
   - <xx输入
   - |过滤
数据在线程中以**事件**形式传递
Logstash会为**事件**添加一些额外信息，如@timestamp

## Logstash语法
- 数据类型
  - 布尔值
  - 字符串
  - 数值
  - 数组
  - 哈徐
- 条件判断
  - 通常使用事件中字段来进行判定
  ```
  filter {
     if [type] == "web" {grok {xxxx}}
    }
  ```
**上面例子的意思是 当经过 过滤器的事件的type字段值为web时使用grok过滤器处理。**
> 对于一些无结构的文本，除了用gork格式化为标准格式，也可以根据其形式将其存入不同的字段中
```
text:
	55.3.244.1 GET /index.html 15824 0.043
filter:
	grok {
    match => { "message" => "%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}" }
  }

输出为:
	client: 55.3.244.1
	method: GET
	request: /index.html
	bytes: 15824
	duration: 0.043
```
- 字段引用
  - [] 可以引用事件中作为关键字段的值如@timestamp就是一个字段
    - 例如从geoip中获得longitude值-> [geoip][location][0]
- 插件
  - codec --> coder+decode
- Grok
> 匹配text的语法为 %{匹配的text属于哪一类型,key_name}%
  - 如logstash没有满足需求的类型，则可有自定义语法
    - 创建目录，规范为patterns
    - 目录中创建一个文件
    - 在这个文件中定义自己的需求 
      `类型名 regular expression`
    ```
    filter {
    grok {
    patterns_dir => ["./patterns"]  //指定定义的文件在哪
    match => { "message" => "%{SYSLOGBASE} %{POSTFIX_QUEUEID:queue_id}: %{GREEDYDATA:syslog_message}" }
   }
   }
   ```
