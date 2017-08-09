# Rsyslog
> Rsyslog是高性能的日志传输收集工具
- 特点
  - 多线程
  - TCP SSL TLS RELP
也是对数据流的处理，像iptables一样对照着策略一条条匹配，匹配哪条就执行哪条操作。
如无匹配，就执行默认策略(RSYSLOG_DefaultRuleset)。一条策略可以包含0至多条规则。一条规则有一个过滤器及一个动作列表组成。


## 配置文件
- 三种格式
  - sysklogd  旧的格式。
```
mail.info /var/log/mail.log
mail.err @server.example.net
```
  - legacy rsyslog 只支持前6版本。$开头
  - Rainscript 最新的格式，非常精准有效
> 目前最推崇的是**RainerScript**
- 注释
  - #
  - /* contents */
- 流控制语法
  - if expr then ...else...
  - stop 停止处理当前信息
  - call 调用策略
  - continue 空操作符
- input 每一个input都需要一个模块
- output 也叫做动作，动作解析方式为action(TYPE='type'...)
  - Type是一个调用插件的名字
- 变量定义
  - set 设置变量
  - unset 取消设置
- 策略的定义(ruleset)
  - 包括rule
eg:
```
ruleset(name="rulesetname") {
    action(type="omfile" file="/path/to/file")
    action(type="..." ...)
    /* and so on... */
}
```
