# 简介
iptables 是用来实现数据包流量控制的与内核中netfilter交互的工具  
只要是进入该节点或者流过等等的包都会经过该节点的netfilter，在其中注册并且表明其方向。再由iptables利用规则决定为每个数据包注册hook，包的hook将决定其流向  

## netfilter
### netfilter的hook种类
- NF_IP_PRE_ROUTING
这个hook会被无论何种方式进入的流量触发。这个hook会在流量被路由前进行相关的处理
- NF_IP_LOCAL_IN
这个hook会被已经被路由到本地，目的地址是本机的流量触发
- NF_IP_FORWARD
这个hook会被已经路由，经历本机要发往其他主机的流量触发
- NF_IP_LOCAL_OUT
该hook会被本地产生的出栈流量触发
- NF_IP_POST_ROUTING
这个hook会被已经路由后的要传出或转发的流量触发。  

### 不同需求传输流量的路径
- 目的地址是本机的包：PREROUTING->INPUT
- 通过该主机，目的地址是其他主机的包：PREROUTING->FORWARD->POSTROUTING
- 本地生成的包：OUTPUT->POSTROUTING

**数据包按照规则进行匹对，最终产生动作或target(-j XXXX的XXX)**  
target通常分为两部分
- 终结targets
终止与链中规则的匹对操作，并将操作权交于netfilter hook
- 未完target
没有终结的target会在对包执行一个操作后会继续执行链中的规则。
### 使用方法
```
iptables [-t 表名] {-A|-C|-D} 链 rule-specification
iptables [-t 表名] -I 链 rule-specification    插入一条或多条规则。可以指定插入的规则号，一般是默认的。
iptables [-t 表名] -R 链 规则序号 rule-specification     -R/--replace 替换链中的规则。
iptables [-t 表名] -D 链 规则号    -D --delete chain 指定的规则/规则号 从链中删除规则。第一条规则是的规则号是1
iptables [-t 表名] -S [链 链序列号]
iptables [-t 表名] {-F|-L|-Z} [链 规则号 参数]  -F/--flush 如果没有指定链，那么会删除表中所有的链 -L/--list 如果没有指定链，则列出所有的规则，可以搭配-n或-v参数使用。 -Z/--zero 如果没有指定链或者链中的规则号，那么会将表中的所有链计数器置0。搭配-L参数可以在清零前，显示出次数。
iptables [-t 表名] -N 链 指定名字，创建一条新的链。
iptables [-t 表名] -X 链  删除一条用户定义的链。
iptables [-t 表名] -P 链 标记  把指定的标记设置为链的策略。只有自带的链才有策略。
iptables [-t 表名] -E 老链名 新链名 -E/--rename-chain 重命名链。
rule-specification = [matches..] [target]    匹配规则包含 match条件，及target
match = -m matchname [per-match-options]     
target = -j targetname [per-target-options]
```  
如果一个包不匹配该规则，那么会继续下一条规则的匹配。如果匹配，通过其target值到跳到指定的下一个规则，这个可以是用户定义的链，或者ACCEPT、DROP、RETURN。  
RETURN:停止匹配该链，从哪跳过来的就回到那个链，并从跳过来的地方下一条执行继续匹配，如果到链尾都未曾被给予通不通过的决策，那么取决于默认策略。  

## 表
> 目前有五张表  
- filter(默认表)
  - INPUT链(负责处理所有目的地址是本机的数据包)
  - FORWARD(处理经过本节点转发的数据包)
  - OUTPUT(处理所有原地址是本机地址的数据包)  
- nat(建立新的连接的包会查询该表)
  - PREROUTING，修改包的目的地址)
  - OUTPUT(和主机发出的数据包有关，在路由器前主机发出包的目的地址)
  - POSTROUTING(在数据包离开防火墙,进行路由判断之后的规则，改变包的源地址)
- mangle(该表专门修改数据包)
> 从kernel 2.4.17版本开始 有两个链。
用来对一些字段进行修改如`TOS、TTL、MARK、SECMARK、CONNSECMARK`。
NARK标记可以为包打上特殊的值，这个值可以被iproute2应用识别，进行不同的路由。也可以基于这个标记进行带宽的限制。
SECMARK标记用来设置安全的标记，用在SELinux中或其他安全系统。CONNSECNARK和SECMARK差不多  
  - PREROUTING(修改在路由前传入的数据包)
  - OUTPUT(修改源地址是本机，但还没有路由的包)
> 内核2.4.18开始，又多了另外三个表  
  - INPUT
  - FORWARD
  - POSTROUTING
- raw(此表在netfilter hook中有较高的优先级)
> 因此在ip_conntrack和其他表之前流过。该表主要配置放行那些打了NOTRACK标记的连接。
  - PREROUTING(通过各种网络接口，到达本地的包)
  - OUTPUT(本地进程生成的包)
- security
> 该表是用来限制MAC地址的规则。例如开启SECMARK和CONNSECMARK标记。这个表在filter表之后调用
  - INPUT
  - OUTPUT
  - FORWARD
## 包的流程
### 当目的地址是本机的包，流入时。其步骤如下  
- 网线传播
- 通过网络接口进入
- 经过`raw`表的`PREROUTING`链
这个链在`connection tracking`发生前进行，可以为其打上特殊的标签，使其不经过`connection tracking`
- 为该包打上`connection tracking`代码
- 流经`mangle`表的`PREROUTING`链
这个链用来修改包。比如修改TOS等待  
- 流经`NAT`表的`PREROUTING`
这个链主要用来做DNAT
- 路由判定
如果目的地址是本机，就流入。如果不是转出
- 流入`mangle`的`INPUT`链
在路由后，发送给本地应用前，对该包进行处理  
- 流入`filter`表的`INPUT`链
来过滤目的地址是本机的所有流量  
- 本地进程或应用

### 原地址是本机
- 本地应用或进程
- 路由判定
原地址是什么，流出的网卡是哪个
- `raw`表的`OUTPUT`链
在`connection tracking`发生前，可以为包打上标记不让其经过`connection tracking`
- 打上标记
- 流入`mangle`表的`OUTPUT`链
不要在这个链上做过滤，会有副作用
- 流入`nat`表的`OUTPUT`链
这个链经常用作对流出包做NAT处理  
- 路由判定
因为之前有了mangle和nat两表，可能会改变包的路由
- 流入`filter`表的`OUTPUT`链
过滤那些从本机流出的包
- 流入`mangle`表的`POSTROUTING`链
这个表的这个链是在包要离开主机前，但是在路由判定后主要的对包进行`mangling`操作。
- 流入`nat`表的`POSTROUTING`链
这就是做`SNAT`的地方、
- 从网卡流出
- 网线传输

### 转发包
- 网线传输
- 网卡流入
- 流入`raw`表的`PREROUTING`链
- 打上标记
- 流入`mangle`表的`PREROUTING`链
- 流入`NAT`表的`PREROUTING`链
- 路由判定，是否是本机还是转发
- 流入`mangle`表的`FORWARD`链
用来做一些特殊的需求，在第一次路由判定后，最后一次前
- 流入`filter`表的`FORWARD`链
做所有的过滤
- 流入`mangle`表的`POSTROUTING`链
- 流入`nat`表的`POSTROUTING`链
做SNAT
- 网卡
- 网线流出

参数：
	这些参数组成规则。规则前面加叹号的，代表取反
	-4/--ipv4
		这个参数对IPtables iptables-restore没有任何影响，如果该参数被插入到ip6tables-restore中，会被忽略。当ipv4和v6 的规则都在同一文件中时才会使用。
	-6/--ipv6
		同上
	[!] -p/--protocol protocol
		该规则中的协议会对包进行检查，可以指定的协议有 "tcp","udp","udplite","icmp","icmpv6","esp","sctp","mh"，或者全部协议"all"。也可以用协议的数字形式代替。可以从/etc/protocols中查看相关协议内容。"all"协议的数字形式为0，代表匹配所以，默认情况下就是all。
	[!] -s/--source address[/mask][,...]
		指定源地址。地址可以是网络名，主机名，一个网络段。也可以使用--src别名。如果这里使用主机名，在将这个规则提交给内核时，那么这里只会解析一次。通过远程DNS来解析这个域名不推荐。可以指定多个的地址，但会拓展成多个规则。
	[!] -d/--destination address[/mask][,...]
		和-s参数语法一致。--dst是其别名
	-m/match match
		使用指定的拓展模块，该模块内部有一些具体的实现参数。
	-j/jump target
		如果包匹配了这条，就可以决定让该包做什么。可以直接给予target值 ACCEPT...等，也可以指定其他链
	-g/--goto chain
	[i] -i/--in-interface name
		接收数据包的网络接口名称。负责进入INPUT、FORWARD和PREROUTING链的包。如果接口名称以"+"结尾，那么所有以这个名字开头的接口都会匹配该规则。如果没有该参数，默认匹配所有接口。
	[i] -o/--out-interface name
		所有发送数据包的网络接口名称，负责进入FORWARD、OUTPUT和POSTROUTING链。+号同-i/--in-interface
	[i] -f/--fragment
		在一些情况，包大于MTU值时会被分段，然后发送，但是第一段中包含包头的完整信息，而后续段中只有部分信息，如果没有此参数，那么可能就只让第一个分段过，后续的分段就不让过了。使用该参数会使规则参照第二段的相应内容来进行处理。如果在-f前加上"!"那么就会只处理包头，或者未分片的包。
	-c/set-counters packets bytes
		在INSERT,APPEND,REPLACE规则时，对包和字节计数器进行初始化。
		
例子
http://www.thegeekstuff.com/2011/06/iptables-rules-examples

-m/--match 参数可以指定的拓展模块


连接或包的状态值:
	INVALID：
		未知的包连接
	NEW：
		一个新的包连接
	ESTABLISHED：
		该包是在已经建立连接的路径中传输的。
	RELATED：
		建立一个新的包连接，但是与已经存在的连接有关。像FTP 数据传输、或者一个ICMP error
	SNAT:
		虚拟状态，源地址不同于包到达目的地址的源地址
	DNAT:
		虚拟状态，目的地址不同于原始的目的地址

icmp：
	当使用 -p/--protocol icmp 时可以使用
	[!] --icmp-type {type|code}[typename]
	可以指定一个ICMP的类型，代表数字，或者ICMP的类型名

iprange：
	给定一个IP地址的随机段
	[!] --src-range from-to
	[!] --dst-range from-to

limt：
	可以限制速率。当达到这个限定速度时，会触发该规则。经常与LOG target组合用来将被限制的内容记录。
	--limt rate[/second/minute/hour/day]
		指定一个包通过的速率。默认为3/hour
	--limt-burst number
		触发limt的阈值。当还没有达到limt限制条件时，到达多少个包就开始触发limt。默认为5

mark：
	匹配与包有关系的netfilter中的mark字段。可以通过下面方法设置target
	[!] --mark value[/mask]
	用给予的mark值匹配包。如果指定了mask，那么则在比较之前先计算 在比较。

multiport：
	这个模块用来匹配一系列的源/目的地址端口。最多可以指定15个端口，指定port1:port2范围的形式视为两个端口。只能在tcp,udp,udplite,dccp和sctp协议中搭配使用
	[!] --source-ports,--sports port[,port|port:port]
	匹配给定端口。多个端口使用逗号分隔。范围端口使用冒号分隔。
	[!] --destination-ports,--dports port[,port|port]
	与--sports使用方法一样
	[!] --ports port[,[port|port:port]
	同时指定匹配源/目的端口
LOG
	让内核记录匹配的包，可以在dmesg或者syslogd来查看那些匹配的包信息。记录日志时，因为没有停止的标签，包会一直遍历接下来的规则。所以一般记录拒绝的包时，用两条规则，第一条 LOG 第二条 DROP
	--log-level
		记录的等级。可以使用数字等级也可以使用名字如：emerg，alert，crit，error，warning，notice，info，debug
	--log-prefix prefix
		设定前缀信息。可以使用29个字母，这样可以在log中更好的发现该记录
	--log-tcp-sequence
		记录TCP序列号
	--log-tcp-options
		记录TCP包头的参数
	--log-ip-options
		记录IP/IPv6包头的参数
	--log-uid
		记录生成这个包程序的用户ID
SNAT
	只做用于nat表的POSTROUTING链和INPUT链。使用该target能够修改包的源地址，并且在以后所有与在这个连接中的包都会如此。
	--to-source [ipaddr[-ipaddr][:port[-port]]
		可以指定一个单独的IP，也可以指定一个范围的IP。如果使用的是tcp,udp,dccp,sctp协议那么端口同样如此。如果没有指定端口的范围，那低于512的源端口将映射为其它低于512的端口。介于512-1023的映射为小于1024的
		至于其他端口会映射为大于等于1024的。
	--random
		随机映射源端口。内核大于等于2.6.21
	--persistent
		替换了SAME target。给予客户端同样的源，目的地址。持久连接
DNAT
REDIRECT
	这个TARGET 只在nat表的PREROUTING和OUTPUT链有效。通过将目的地址改变成来时物理接口的地址，从而将包重定向到机器本身。
	--to-ports port[-port]
		指定目的地址的端口或者一个范围的端口。如果没有该选项，那么目的地址端口不改变。只对tcp、udp、dccp、sctp协议有效
	--random
		随机映射端口 内核大于等于2.6.22
MASQUERADE
	只在nat表，POSTROUTING链有用。被应用在动态分布的IP上。如果是静态IP那么使用SNAT。MASQUERADE能够将网卡地址映射给包，让包出去。
	--to-ports port[-port]
		指定一些端口，覆盖原端口。只有 tcp udp dccp 或 sctp协议有效
	--random
		随机映射源端口。内核大于等于3.7才能使用
