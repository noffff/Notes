SNMP是基于TCP/IP架构之上的。<br>
分为管理设备(Port 162)和被管理设备(代理进程.agent Port 161)
## 组件
- MIB(管理信息库)
包含所有代理进程所有可查询和修改的参数
- SMI(关于MIB一套公用的结构和表示符号)
- 管理进程和代理进程之间的通信协议
SNMP 简单网络管理协议
> SNMP通常采用UDP，所以应用层要有重传和超时机制
## 报文
> 管理端和代理进程之间交互使用以下五种报文
- get-request
从代理进程中提取一个或多个参数值
- get-next-request
从代理进程处提取一个或多个参数的下一个参数值
- set-request
设置代理进程的一个或多个参数值
- get-response
返回一个或多个参数值
- trap
代理进程主动发出报文，表示有事情发生
---
## SNMP报文中一些常用的字段
- PDU类型
  - 0 get-request
  - 1 get-next-request
  - 2 get-response
  - 3 set-request
  - 4 trap
- 差错状态
  - 0 noError 没有错误 
  - 1 tooBig 代理进程无法把响应放在SNMP消息中发送
  - 2 noSuchName 操作一个不存在的变量
  - 3 badValue set操作的值或语法有错
  - 4 readOnly 管理进程试图修改只读变量
  - 5 genErr 其他错误
## 对象标识符
指明一些命名的对象。通过"."分隔。树状结构类似DNS和Unix文件系统<br>
该命名对象已经是权威机构授权过得。不能乱分配。
每一位对应一个组织或结构。一般对于一个变量，会在最后加".0"来处理
