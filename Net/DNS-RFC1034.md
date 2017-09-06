# DNS
## 设计目标
构造一个namespace映射网络的资源。为了避免编码的问题name中不包含网络字符、地址、路由等其他类似的信息<br>
因为DNS数据的规模以及其更新频率，注定了其必须使用分布式，本地缓存的方式来提高性能。<br>
"domain"和"domain name"都经常被用在DNS描述的文章中，"domain name"被用在一个通过"."符表示结构的名称中。与DNS无关
另一方面，从查询速度和耗时的权衡考虑，所有的数据都通过被打了类型标签的name联系。查询时可以通过制定一种类型来规定查找的范围。<br>
因为使用者可能会在不同类型的网络和应用进行查询等操作，DNS提供这种支持。能够将所有数据打上类的标签，以至于在不同环境中进行操作。<br>
在系统中数据的交换是比较慢的，但是在DNS这个系统中通过分布式策略，其交换速度非常快。<br>
边界管理负责将数据库的响应分散开，将响应分散到一个或多个主机上。并且有义务提供冗余的访问<br>
域系统中的客户端应该能够识别之前信赖的nameserver，然后可以信赖这个nameserver引入的，不在信任列表的其它nameserver<br>
nameserver的服务性比起信息一致性更为重要，因此其更新进程一般通过域系统用户的渗透更新而不是对所以副本进行统一更新。更新失败会造成网络和主机的解析失败<br>
在一个拥有分布式数据库、一个name server的系统中，可能会接到一个查询自己不能解析，但其他nameserver能够处理的请求。对于这种请求有两种解决方法。
- 递归<br>
该namesver会代替client向其他nameserver查询，直到拿到结果返回给client<br>
- 迭代<br>
该namesver会使client去请求其他namesver。
> 默认的方法是迭代查询，带支持递归查询<br>
域名系统假设所有的数据都源于域系统中多个主机的中的master文件。master文件会被各个主机的本地系统管理员管理更新。master文件是一个文本文件。nameserver可以加载master文件，通过nameserver来使一个domain系统变的有效。用户端可以使用一个叫做**resolver**的标准进程访问nameserver<br>
标准的master文件可以在主机间通过多种方式进行进行交换(如FTP、mail或者其他机制)。用户可以利用该特征在不构建namesver的前提下，实现一个域(master文件)，然后通过一个运行nameserver的外部主机对该master文件的加载。<br>
每个主机的管理员可以在本地配置nameserver以及resolvers(RFC-1033).对于一个nameserver，配置的数据包括本地master文件的认证以及外部服务加载的指令。外部服务的nameserver使用该master文件或者副本来加载zones。<br>
域系统定义对于访问数据及引入其他nameserver的策略。同时也定义了cache查询到的数据以及系统管理员定期刷新数据的周期<br>
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
是一个特殊的树形结构的命名空间，并且其中的数据与name有关联。树上的每个节点或叶子都是命名空间树的一个信息集合，查询操作是使用集合中的一个特殊类型，来提取集合中的一些特殊信息<br>
- Name server
一个服务，用来负责domain树结构和信息，可以cache domain树任意部位的结构或信息。通常一个特殊的nameserver包含一个domain space 子集（叶子/节点）完整的信息，并且有一个指向其它name server的指针。name server知道自己包含那一部分domain 树的信息。它们会作为这个部分的**权威authority**存在，有权威信息的组织单元被叫做"zone",这些zone可以自动分发到为zone的数据提供冗余服务的name server中<br>
从Name server角度来看，domain 系统是由多个叫做zone的本地信息集合组成的。name server有一个或多个zone的本地副本。name server必须周期性的刷新其zone，必须支持并发查询<br>
- Resolvers
能够从name server对client请求的响应中提取信息的进程。resolver至少能够访问一个name server并且可以使用name server的信息直接的回答查询请求。

### Domain Name space 和资源记录
#### Name space空间结构和组成和术语
Domain name space是一个树形结构，每个节点和叶子都对应一个资源集合(可能为空)。
Domain 树中每个节点都有label，从0到63(八进制),相邻节点不能有同样的label，不相邻的可以使用一样。root节点的label为空。<br>
Domain name是从节点的label到root节点的label列表。组成domain name的label从左到右进行读取，也是从最低到最高层。<br>
应用内部将域名转换为有序的的label。每个label的八字节长度后跟随八字节的字符。因为所有Domain name的root(空字符的label)结尾，所以在应用内部可以使用一个零长度的来表示一个domain name的完结。一般讲，domain name可以随意存储，现在域名的书写方式都是不区分大小写。<br>
用户输入domain name时，会省略每个label的长度，并且label会使用"."分隔。一个完整的Domain name都以rootlabel结尾，这种形式往往通过在doamin name尾部加"."表示。通过使用这种属性，可以分辨下列内容:;- 一个绝对 Domain name或完整Domain name，如 "test.test.com."
- 不完全的domain name，通过使用local domain来补全。这种方式加做"relative"<br>
relative name可以使用较为有名的orgion也可以使用Domain 列表作为搜索列表。relative name大多数都是用户自己定义的。在master 文件中，通常会使用单独的origin domain name。<br>
为了简化这个实现过程，Domain name的所有字符被限制在255字节<br>
一个域由一个doamin name以及指定Domain name以及在domain name下指定的domain组成。如果一个域包含另一个域，那么被包含的域就是这个域的子域。可以通过检查子域名的结尾是否包含了该域的域名来确认两域的关系，如A.B.C.D是B.C.D、C.D、D和root域的子域<br>
DNS没有特殊的树结构，掉label也没有特殊的选择规则。这些使DNS能够适应于各种应用结构中。
