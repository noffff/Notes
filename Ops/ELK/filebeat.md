- 工作方式
  - 原理图
![](https://www.elastic.co/guide/en/beats/filebeat/current/images/filebeat.png)
  - Harvest 对每个文件一行一行的读取，并将内容发送至output,为每个打开的文件保留描述符
    - 通过定义"scan_frequency"来决定扫描的频率
  - Prospector 管理Harvest并且找到要读的文件，对每个文件都有独一的标识符，不只依赖于文件名和路径，因为会改变。
  - registry 将读到文件偏移量存储在该文件中。运行时存于内存，进程停止时存于磁盘
  - 数据成功的发送到output阶段时，output会返回一个ack来表示数据成功传输。如果在数据发送时filebeats关掉了，没有收到ACK，不管数据有没有成功发送，filebeats重启时都会再次发送一遍
- Bug
  - 目前filebeats的环境变量，如果使用systemd不能使用全局变量，如果使用命令行启动则可以
- spool
  - spool-size 指定spool大小，当事件在spool中攒够这么多到会强制推送，
  - idle -time 达到这个值就提交
- drop 能够根据指定条件排除event，field。也能在满足指定条件时加上field。
  - drop event
```
processors:
 - drop_event:
     when:
        condition
```
  - drop fields  @timestamp和type字段是不会被丢弃的
```
processors:
 - drop_fields:
     when:
        condition
     fields: ["field1", "field2", ...]
- drop_fields:    测试这种方式好用
    fields: ["field1",...]
    when.contains.xxx: xxxx
```
  - include fields<br>conditions
```
processors:
 - include_fields:
     when:
        condition
     fields: ["field1", "field2", ...]
```
## Conditions
每个判断条件都会收到字段，对每个字段处理。如果一个条件处理多个字段使用**AND**
```
processors:
 - <processor_name>:
     when:
        <condition>
     <parameters>
 - <processor_name>:
     when:
        <condition>
     <parameters>
```
- equals   判断字段的值是否与其相等
```
equals:
  http.response.code: 200
```
- contains 判断字段值是否包含
```
contains:
  status: "Specific error"
```
- regexp 通过正则匹配
```
regexp:
  system.process.name: "foo.*"
```
- range 对字段值范围的检查
  - lte,lt
  - gte,gt
```
range:
    http.response.code:
        gte: 400
range:
    system.cpu.user.pct.gte: 0.5
    system.cpu.user.pct.lt: 0.8
```
- or 
```
or:
  - equals:
      http.response.code: 304
  - equals:
      http.response.code: 404
```
- and 
```
and:
  - equals:
      http.response.code: 200
  - equals:
      status: OK
```
**<condition1> OR <condition2> AND <condition3>**
```
or:
 - <condition1>
 - and:
    - <condition2>
    - <condition3>
```
- not
```
not:
  equals:
    status: OK
```
开启多prospector
filebeat.prospectors:
- type: log
    paths:
- type: log1
    paths:
      - /var/log/*/*.log 该路径不包括/var/log/*的文件

目前type类型
	log、stdin、redis
paths:
	存放日志的目录地址

recursive_glob:
	默认关闭，开启后 **会拓展  foo** --> foo/ foo/*   foo/*/*  一个 ** 能扩张深度为8

encoding:
	读文件的编码

exclude_lines:
	排除的行，正则。如果开启了multiline，会在组成单独的一行前，进行过滤。下同
	https://www.elastic.co/guide/en/beats/filebeat/master/regexp-support.html

include_lines:
	保留的行，默认全保留。

如果上述都开启，那么先  include 再 exclude

exclude_files:
	排除的文件，

tags:
	会给指定的一系列内容打上tag，便于处理
	example:
		filebeat.prospectors:
		- paths: ["/var/log/app/*.json"]
		  tags: ["json"]

fields:
	可以为output加入的 字段信息。能够方便过滤。
	标量, 数组, 目录, 任意深度嵌套都可以。
	e.x
	 filebeat.prospectors:
	 - paths: ["/var/log/app/*.log"]
	   fields:
	     test: ttttt
	这种方式加的字段，会处于fields字段下，如果要让用户定义字段在output中成为独立的字段需要设置fields_under_root=true

ignore_older:
	该值能够防止很早以前的日志修改后，触发再次传送。指定一个时间字符 例如 2h
	该值要大于 close_inactive

close:
	有各种close类别，是根据对其日志收集完后的时间来做判据

json:
	将JSON格式信息解码。filebeats是论行处理，如果没一行都是一个JSON对象，那么就正好解析了。解码在行和多行过滤之前
	ex:
	  json.keys_under_root: true
          json.add_error_key: true
          json.message_key: log 

keys_under_root:
	默认json数据解码后，会在document段放一个json标签，如果开启这个值，会在消息最顶层放置。

add_error_key:
	会将哪些带 log关键字，但不能解析的信息中加上 error.message" and "error.type: json的字段

message_key:
	用于行和多行过滤的顶级关键字，必须是一串字符。否则会引起差错

multiline:
	开启多行模式

tail_files:
	开启后就从文件尾开始读文件。该模式要移除原有registry。

spool_size:
	spool的大小。
https://www.elastic.co/guide/en/beats/filebeat/master/configuration-filebeat-options.html
