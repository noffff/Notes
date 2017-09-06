```
input {
    beats {
        port => "5043"
    }
}
filter { //过滤器 可有可无参数
    grok {
        match => { "message" => "%{COMBINEDAPACHELOG}"}
    }
}
output {
    stdout { codec => rubydebug }
}
```

除了上述插件外，如果想保存日志则可在output段，插入
file {
	path => "writing data to someplace"
}
对于多输入，则可有在input段中插入额外的,都有哪些插件在以后补全。
