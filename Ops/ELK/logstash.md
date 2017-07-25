Logstsh实现的功能就类似 cat xxx|awk xxx|tee xxx(除此外还支持解码，编码)。cat就类似Logstash中的输入，awk类似filter，tee类似输出<br>
- 简单的教程
  - 从终端标准输入获得输入，将输出定向到标准输出
```
logstash -e 'input{stdin{}}output{stdout{codec=>rubydebug}}'
输入 hello world 会输出
{
    "@timestamp" => 2017-07-23T13:06:41.003Z,
      "@version" => "1",
          "host" => "vm1",
       "message" => "hellow world"
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
## Logstash的线程
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
- 字段引用
  - [] 可以引用事件中作为关键字段的值如@timestamp就是一个字段
    - 例如从geoip中获得longitude值-> [geoip][location][0]

- 插件
  - codec --> coder+decode
