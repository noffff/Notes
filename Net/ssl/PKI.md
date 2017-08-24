# PKI
## 公钥基础设施<br>
PKI是一大类，常用的是internet PKI和WEB PKI<br>
基于X509标准的叫做PKIX。X509是WEB 证书等的标准<br>
## PKI体系结构
一般根CA都是离线的，用来签署二级CA(intermediate CA)进行在线签署工作<br>
根CA离线是为了让根私钥断绝外界访问，从而保证根CA的安全<br>
- 服务商/实体/订阅人(好多种叫法，通指面向Client端如游览器的服务)<br>
实体，需要证书来证明或提供安全服务的服务
- 登记机构<br>
**registration authority**(RA),用来完成证书签发的一些相关管理工作，校验身份等<br>
经其处理完才交于CA签发证书。只有大型CA架构才会用到
- 证书颁发机构<br>
**certificate authority**(CA),合法的证书颁发机构。用来为实体/服务签发证书<br>
同时也维护签发证书的合法性(通过吊销证书维护)。<br>
- 信赖方<br>
使用证书的团体。比如游览器。一般游览器，操作系统，软件会默认包含一个根证书库<br>
一般用这个根证书库来校验服务的可信度

### 签发流程
```
将用户身份信息、用户公钥信息。按照特定格式组成数据D
用摘要算法对数据D进行计算得到摘要H
使用CA私钥对摘要H进行加密得到数字签名S
将用户信息、用户公钥信息、数字签名S按照特定格式组合成数字证书
```
## 证书
数字签名的实体。根据不同Keyusage实现不同功能<br>
证书在服务端和客户端的认证流程
```
实体证书包括了公钥、使用信息等。证书需要签名的机构公钥解析(证书)解析后可获得
服务的公钥，用这个公钥可以解析实体密钥签名的消息，进行进一步的验证
```
### 证书字段
> 证书由很多字段组成，随着证书版本(SSL版本)的提升字段也相应得到提升，v3版本添加了扩展字段
通过拓展字段可以大大提高证书的工作范畴。如一个证书通过拓展字段指向多个域名;
- 版本<br>
1、2（增加两个标识符）、3（增加拓展功能）<br>
v3版本现在是正在使用的版本
- 序列号<br>
CA签发过的证书的序列号会保存在其数据库中，也是CA用作识别证书的唯一标识符<br>
- 签名算法<br>
签名使用的什么算法
- 颁发者<br>
指出证书颁发者的可分辨名称(distinguished name)DN<br>
DN包括很多可选字段，根据不同实体使用的不同<br>
如 C(国家) O(组织)等
- 有效期
- 使用者<br>
使用者的实体/服务的实际名称、域名。但最初CN会使用WEB服务的域名<br>
但为了能匹配多个主机名现在使用扩展名称，该字段可以不用、舍弃
- 公钥<br>
包含公钥，使用者实体的公钥
## 证书扩展字段
> 如果某个扩展字段被设为关键扩展，那么客户端必须能够解析和处理。
否则拒绝证书<br>
X509v3 extensions:
```
X509v3 Extended Key Usage:
    TLS Web Server Authentication
X509v3 Basic Constraints: critical
    CA:FALSE
X509v3 Subject Key Identifier:
    D2:E6:0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx87:FA:DD
X509v3 Authority Key Identifier:
    keyid:C0:C3:1F:7E:B8:xxx:27:xxx:A7:48:5A:12xxxxxxxx56:F5:C7

Authority Information Access:
    OCSP - URI:http://ocsp.xxxxxx.cn

X509v3 Subject Alternative Name:
    DNS:xxxx.xxxx.com
X509v3 CRL Distribution Points:

    Full Name:
      URI:http://crl.xxxxx.cn/crl
```
扩展字段包含唯一的**对象标识符**OID、关键扩展标志器以及ASN.1值
- Subject Alternative Name<br>
用于替换**CN**字段，能够处理多个域名或其它身份信息<br>
简而言之就是一个证书通过这个字段可以指定多个服务地址
- Extended Key Usage<br>
能够限制签发证书对象的功能和权限,不在扩展字段也有该项的值，但所指功能范围不同<br>
- (Basic Constraints)<br>
表明证书是否为**CA证书**，只有CA证书级别才能对其他证书签名。<br>
可以通过**路径长度**约束字段，限制二级CA证书向下签发证书的深度<br>
- CRL分发点(CRL Distribution Points)<br>
通过该字段确定CRL的LDAP或HTTP URL地址，一个证书最少有一个CRL或OCSP信息
- 颁发机构信息访问(Authority Information Access,AOA)<br>
该字段提供如何访问签发CA提供的额外访问信息和服务，比如OCSP url
- 使用者密钥标识符(Subject Key Identifier)<br>
唯一值，识别包含特别公钥的证书。所有证书必须都有该字段。该值要与CA签发证书的授权密钥标识符值一致。
- 颁发机构密钥标识符(Authority Key Identifier)<br>
唯一值，必须与颁发机构的使用者密钥标识符的信息一致<br>

> CRL地址不用https，因为如果用了https会面临先有鸡先有蛋问题
## 证书链
多数情况下，一个子证书的签发是经过几层CA的。为了完美验证<br>
服务器需要提供一个证书链来一步一步验证到可信根证书<br>
- 交叉证书<br>
为了让一个新的CA立马起效，不可能将其新的根证书立刻广泛部署。<br>
通常使用的方式是使用一个已经内置的CA对该CA的根密钥进行进行签名。
服务器一次只能提供一条证书链
## 证书生命周期
在CSR文件提交给CA时已经开始。CSR包括公钥信息并且拥有订阅人服务的对应私钥签名<br>
CA一般会覆盖CSR文件中的一些内容，并将其他信息置入到证书中<br>
CA根据不同证书申请，执行不同验证流程<br>
- 域名验证<br>
DV 证书需要CA验证订阅人对域名的所有权之后进行签发。
- 组织验证<br>
OV 证书会对身份和真实性进行验证，将这些信息编码到证书中存在前后不一致情况
- 扩展验证<br>
EV 更加严格的要求验证身份和真实性，解决OV前后不一致。
## 吊销证书
两种方式
- CRL 证书吊销列表<br>
一组未过期，但被吊销证书序列号的列表。CA维护一个或多个这样的列表<br>
CRL会随着时间增加，越来越大 查询越来越慢，并且一般客户端会缓存该列表不实时
- OCSP 在线证书状态协议<br>
支持实时查询。允许信赖方获得一张证书的吊销信息。<br>
一般可以启动一个OCSP服务，然后开启OCSP stapling扩展。<br>
服务器使用该特性将证书是否过期的信息返回给客户端<br>
开启OCSP stapling的服务在Server say Hello的过程中返回一个**status_request**扩展<br>
> 一般游览器默认不查非EV的CRL.OCSP响应会影响到WEB的访问速度。目前使用OCSP tapling只支持一次
OCSP响应，用于检测证书的吊销情况。 
chrome、火狐目前默认忽略OCSP的检测。但开启OCSP stapling<br>
## 创建证书
证书名要能匹配域名的不同类型及子域名,否则会认证失败<br>
如www.test.com不能匹配test.com。如果访问一个服务通过一个DNS解析的域名访问，那么证书要包括这个被DNS解析的域名<br>
泛域名：*.test.com,不妨为匹配一个大类的解决方案<br>
- 生成密钥<br>
密码:在生成密钥时会提示输入密码，该密码只是在储存副本密钥等情况有用。应用通过密码验证后会把私钥明文保存在程序内存中，利用其它手段从内存中拿不用密码<br>
`openssl genrsa -aes128 -out one.key 2048`
- 创建证书签名申请<br>
创建的CSR是用来提交给CA的正式申请<br>
该申请包含申请证书的实体(服务)公钥以及实体的某些信息。该数据会成为证书一部分<br>
CSR用其包含的公钥所对应的私钥进行签名
`openssl req -new one.key -out one.crs`
如果需要创建多个主机名有效的证书<br>
两种方法
- 泛域名<br>
*.test.com
- x509的**使用者可选名称**(subject alternative name)<br>
在该字段中列出所有要使用的主机名<br>
一般讲该字段包含的内容写入文件如
one.ext
```
subjectAltName = DNS:*.test.com,DNS:test.com
```
> 真正环境使用时会设置顶级域名以及其泛域名两项
`openssl x509 -req -days 365 -in one.csr -signkey one.key -out one.crt -extfile one.ext`

