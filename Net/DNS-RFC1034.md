# DNS
## 设计目标
构造一个namespace映射网络的资源。为了避免编码的问题name中不包含网络字符、地址、路由等其他类似的信息  
因为DNS数据的规模以及其更新频率，注定了其必须使用分布式，本地缓存的方式来提高性能。  
"domain"和"domain name"都经常被用在DNS描述的文章中，"domain name"被用在一个通过"."符表示结构的名称中。与DNS无关
另一方面，从查询速度和耗时的权衡考虑，所有的数据都通过被打了类型标签的name联系。查询时可以通过制定一种类型来规定查找的范围。  
因为使用者可能会在不同类型的网络和应用进行查询等操作，DNS提供这种支持。能够将所有数据打上类的标签，以至于在不同环境中进行操作。  
在系统中数据的交换是比较慢的，但是在DNS这个系统中通过分布式策略，其交换速度非常快。  
边界管理负责将数据库的响应分散开，将响应分散到一个或多个主机上。并且有义务提供冗余的访问  
域系统中的客户端应该能够识别之前信赖的nameserver，然后可以信赖这个nameserver引入的，不在信任列表的其它nameserver  
nameserver的服务性比起信息一致性更为重要，因此其更新进程一般通过域系统用户的渗透更新而不是对所以副本进行统一更新。更新失败会造成网络和主机的解析失败  
在一个拥有分布式数据库、一个name server的系统中，可能会接到一个查询自己不能解析，但其他nameserver能够处理的请求。对于这种请求有两种解决方法。
- 递归  
该namesver会代替client向其他nameserver查询，直到拿到结果返回给client  
- 迭代  
该namesver会使client去请求其他namesver。
> 默认的方法是迭代查询，带支持递归查询  
域名系统假设所有的数据都源于域系统中多个主机的中的master文件。master文件会被各个主机的本地系统管理员管理更新。master文件是一个文本文件。nameserver可以加载master文件，通过nameserver来使一个domain系统变的有效。用户端可以使用一个叫做**resolver**的标准进程访问nameserver  
标准的master文件可以在主机间通过多种方式进行进行交换(如FTP、mail或者其他机制)。用户可以利用该特征在不构建namesver的前提下，实现一个域(master文件)，然后通过一个运行nameserver的外部主机对该master文件的加载。  
每个主机的管理员可以在本地配置nameserver以及resolvers(RFC-1033).对于一个nameserver，配置的数据包括本地master文件的认证以及外部服务加载的指令。外部服务的nameserver使用该master文件或者副本来加载zones。  
域系统定义对于访问数据及引入其他nameserver的策略。同时也定义了cache查询到的数据以及系统管理员定期刷新数据的周期  
- 系统管理员权利
  - 定义zone边界
  - master文件
  - 升级master文件
  - 刷新的策略
- 域系统提供
  - 资源数据的标准格式
  - 查询数据库的标准方法
  - 从外部nameserver获取数据刷新本地nameserver数据的方法

## DNS原理
### DNS三大组件
- Domain Name Space命名空间 和资源记录
是一个特殊的树形结构的命名空间，并且其中的数据与name有关联。树上的每个节点或叶子都是命名空间树的一个信息集合，查询操作是使用集合中的一个特殊类型，来提取集合中的一些特殊信息  
- Name server
一个服务，用来负责domain树结构和信息，可以cache domain树任意部位的结构或信息。通常一个特殊的nameserver包含一个domain space 子集（叶子/节点）完整的信息，并且有一个指向其它name server的指针。name server知道自己包含那一部分domain 树的信息。它们会作为这个部分的**权威authority**存在，有权威信息的组织单元被叫做"zone",这些zone可以自动分发到为zone的数据提供冗余服务的name server中  
从Name server角度来看，domain 系统是由多个叫做zone的本地信息集合组成的。name server有一个或多个zone的本地副本。name server必须周期性的刷新其zone，必须支持并发查询  
- Resolvers
能够从name server对client请求的响应中提取信息的进程。resolver至少能够访问一个name server并且可以使用name server的信息直接的回答查询请求。

### Domain Name space 和资源记录
#### Name space空间结构和组成和术语
Domain name space是一个树形结构，每个节点和叶子都对应一个资源集合(可能为空)。
Domain 树中每个节点都有label，从0到63(八进制),相邻节点不能有同样的label，不相邻的可以使用一样。root节点的label为空。  
Domain name是从节点的label到root节点的label列表。组成domain name的label从左到右进行读取，也是从最低到最高层。  
应用内部将域名转换为有序的的label。每个label的八字节长度后跟随八字节的字符。因为所有Domain name的root(空字符的label)结尾，所以在应用内部可以使用一个零长度的来表示一个domain name的完结。一般讲，domain name可以随意存储，现在域名的书写方式都是不区分大小写。  
用户输入domain name时，会省略每个label的长度，并且label会使用"."分隔。一个完整的Domain name都以rootlabel结尾，这种形式往往通过在doamin name尾部加"."表示。通过使用这种属性，可以分辨下列内容:;
- 一个绝对 Domain name或完整Domain name，如 "test.test.com."
- 不完全的domain name，通过使用local domain来补全。这种方式加做"relative",在*nix的resolve.conf中的search 就是要补全的内容    
relative name可以使用较为有名的orgion也可以使用Domain 列表作为搜索列表。relative name大多数都是用户自己定义的。在master 文件中，通常会使用单独的origin domain name。  
为了简化这个实现过程，Domain name的所有字符被限制在255字节  
一个域由一个doamin name以及指定Domain name以及在domain name下指定的domain组成。如果一个域包含另一个域，那么被包含的域就是这个域的子域。可以通过检查子域名的结尾是否包含了该域的域名来确认两域的关系，如A.B.C.D是B.C.D、C.D、D和root域的子域  
DNS没有特殊的树结构，掉label也没有特殊的选择规则。这些使DNS能够适应于各种应用结构中。

## 资源记录
一个domain name定义一个节点，每个节点有很多组资源信息。每一条都简称为RR。一个RR有以下几个特性  
- owner
名称
- type
16字节的编码值，这个值指定了资源记录中资源的类型。
  - A
主机地址
  - CNAME 
别名，可以将多个指向一个,这样在变动时只需要改变这一个就可以改变多个
  - HINFO
表示主机使用的CPU和OS
  - MX
mail交换
  - NS
该Domain的权威名字服务器
  - PRT
指向域名的另一命名空间的指针
  - SOA
识别一个权威zone的开始


- class
16字节的编码值，用来识别一个协议族或实例的协议
  - IN
网络系统
  - CH
????the Chaos system


- TTL
一个RR有效的时间，32位字节，单位为秒。主要用来规定resolver缓存这条记录的有效时间，超过丢弃。  
该限制对权威zone的数据无效。0为不缓存


- RDATA
type和class用来描述记录时依赖的数据段
  - A
对于`IN` class来说，是一个32位的IP地址
对于`CH` class来说，一个域名跟随一个16为的8进制的Chaos address
  - CNAME
一个域名
  - MX
16位的优先值，越低越权重越高。通常跟一个主机名，并且经常用在mail交换时后端所有域的权重
  - NS
一个主机名
  - PTR
一个域名
  - SOA
一些字段  
RDATA字段中的RR的部分数据会作为二进制字符串和域名中的一部分。Domain name在DNS中经常会被当做指向其他数据的指针  
在DNS协议的包中，RR请求以二进制的形式存在并且经常使用更高阶的编码格式存储在name server或者resolver  
RR可以使用一行，也可以在括号中使用多行  
一行开始会是该RR的要解析的东西(可以成为RR的所有者)，如果为空白则假设与上一行的RR所有者相同(该形式可读性更加高)。  
一个RR的结构  
RR所有者(被解析对象)  class type rdata  

## 别名
通常主机名或者其他资源可能在一个资源中以多种名字出现。如许多组织提供的邮箱，真正解析到的都是一样的邮箱。这些名字中只有一个是真正的资源名，其他都是别名。  
doamin系统提供了对于别名的特征提供了一个CNAME资源记录。一个CNAME RR将别名作为这个RR的所有者，并将真正的域名/地址放在RDATA。
如果一个节点上存在一条CNAME RR，那么该节点就不能存在其他数据。这条规则确保了资源名与其别名是一绝对一致的。
在DNS软件中CNAME RR会引起一些特别的操作。当一个name server使用doamin name不能找的需要的RR记录，他会去检查有没有与要查询的RR class相同的CNAME name。如果有name server会将CNAME 记录放在response中并且重新查询指定的Domain name的CNAME 记录的数据字段。当查询到与CNAME type相同的记录时，不重新开始  
例子:
    假设一个name server处理一个`USC-ISIC.ARPA.ARPA`查询A信息的请求，而RR如下所示  
```
 USC-ISIC.ARPA  IN	 CNAME     C.ISI.EDU
 C.ISI.EDU 	IN 	 A         10.0.0.52
```   
这些RR会用来回复这个A查询，如果 只是一个CNAME或*查询只会恢复CNAME记录  
在RR中其他名字指向的一条记录的名字应该是真正的名称，而不是别名。这避免在访问信息时得到一些额外的信息。  比如按照上面的记录那么ARPA记录应该如下  
```
52.0.0.10.IN-ADDR.ARPA IN PTR C.ISI.EDU
```
按照鲁棒原理，当遇到一个CNAME 链或者循环时Domain软件不会报错。不过会发出一个`error`信号`  
互联网中，查询请求通过使用UDP数据包或者TCP连接传输。一般情况，用户不直接生成查询，通常会去请求一个resolver，由其进行处理，向name server发送请求等。  
DNS请求和响应都标准的消息形式，消息头有一些可变的字段，通常情况是四块，携带查询请求和RR。  
在消息头中最重要的四个字节字段叫做操作码。不同的查询被分割开来。  
四个字段为：  
- Question
携带查询的name和其他查询参数
- Answer
携带回答查询的响应
- Authority
携带RR，用来描述其他权威服务器，有时对于权威的数据 会在`answer`块中携带SOA RR
- Additional  
携带可能对其它块中正在使用的RR有帮助的信息  


