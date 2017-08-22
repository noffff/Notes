# PKI
公钥基础设施<br>
PKI是一大项，其中包括常用的internet PKI及WEB PKI
## PKI体系结构
一般根CA都是离线的，用来签署二级CA(intermediate CA)进行在线签署工作
- 订阅人<br>
实体，需要证书来证明或提供安全服务的服务
- 登记机构<br>
**registration authority**(RA),用来完成证书签发的一些相关管理工作，校验身份等<br>
经其处理完才交于CA签发证书
- 证书颁发机构<br>
**certificate authority**(CA),人们信赖的证书颁发机构。用来为已确认的用户签发证书<br>
也在线提供其签发证书的吊销信息<br>

**签发流程**
```
将用户身份信息、用户公钥信息。按照特定格式组成数据D
用摘要算法对数据D进行计算得到摘要H
使用CA私钥对摘要H进行加密得到数字签名S
将用户信息、用户公钥信息、数字签名S按照特定格式组合成数字证书
```
- 信赖方<br>
使用证书的团体。比如游览器。一般游览器，操作系统，软件会默认包含一个根证书库<br>
一般用这个根证书库来校验服务的可信度
# 证书
## 证书字段
> 证书有一些字段组成，v3包括扩展字段
- 版本<br>
1、2（增加两个标识符）、3（增加拓展功能）
- 序列号<br>
作为CA用来校验其是否为自己颁发的唯一标识符
- 签名算法<br>
签名使用的什么算法
- 颁发者<br>
指出证书颁发者的可分辨名称(distinguished name)DN<br>
DN包括很多可选字段，根据不同实体使用的不同<br>
如 C(国家) O(组织)等
- 有效期
- 使用者<br>
使用者是实体(服务)的可分辨名称，最开始CN字段会使用WEB服务的域名<br>
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
- 使用者可选名称<br>
用于替换**使用者**字段，能够处理多个域名或其它身份信息<br>
简而言之就是一个证书通过这个字段可以指定多个服务地址
- 名称约束<br>
能够限制签发证书对象的功能和权限
- 基础约束(Basic Constraints)<br>
表明证书是否为**CA证书**，只有CA证书级别才能对其他证书签名。<br>
并且通过**路径长度**约束字段，限制二级CA证书向下签发证书的深度<br>
- 密钥用法(Key usage)扩展密钥用法(extended key usage)<br>
设置证书应用的场景。CA证书一般为**证书签名照**、**CRL签名者**
- 证书策略<br>
包含一个或多个策略，一个最后的子证书至少包含一条策略，表明证书在何种条款下签发
- CRL分发点(CRL Distribution Points)<br>
通过该字段确定CRL的LDAP或HTTP URL地址，一个证书最少有一个CRL或OCSP信息
- 颁发机构信息访问(Authority Information Access,AOA)<br>
该字段提供如何访问签发CA提供的额外访问信息和服务，比如OCSP url
- 使用者密钥标识符(Subject Key Identifier)<br>
唯一值，识别包含特别公钥的证书。所有证书必须都有该字段。该值要与CA签发证书的授权密钥标识符值一致。
- 授权密钥标识符<br>
签发此证书的CA的唯一标识符。用于在构建证书链时找到颁发者的证书
- 颁发机构密钥标识符(Authority Key Identifier)<br>
唯一值，必须与颁发机构的使用者密钥标识符的信息一致<br>

> CRL地址不用https，因为如果用了https会面临先有鸡先有蛋问题
## 证书链
多数情况下，一个子证书的签发是经过几层CA的。所以说为了认证该子证书，只有单一的CA是不能验证的。<br>
所以服务器需要提供一个证书链来一步一步验证到可信根证书<br>
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
CRL会随着时间增加，越来越大 查询越来越慢
- OCSP 在线证书状态协议<br>
支持实时查询。允许信赖方获得一张证书的吊销信息。

## 创建证书
证书名要不能匹配域名的不同变体<br>
如www.test.com不能匹配test.com。如果有DNS解析指向域名，证书要包括这个DNS指向的域名<br>
泛域名：*.test.com
使用开源的OpenSSL
生成加强版的私钥<br>
创建证书签名申请CSR并发送给CA<br>
在WEB服务器安装CA提供的证书<br>
等等
- 生成密钥<br>
密钥算法:RSA\DSA\ECDSA
密钥长度:RSA 2048\ECDSA 256
密码:该密码只是在储存副本密钥等情况有实际用处。因为应用通过密码验证后会把私钥明文保存在程序内存中
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

## 创建私人CA
一般根CA下有intermediate CA用来进行签发实体证书<br>
创建私人CA比较复杂，有配置文件比较简单<br>
[配置文件](https://github.com/ivanr/bulletproof-tls/blob/master/private-ca/root-ca.conf)
- 根CA<br>
```
# mkdir certs db private
# echo 1001 > db/crlnumber
# openssl rand -hex 16 >db/serial
```
  - 生成根CSR<br>
`# openssl req -new config root.conf -out root-ca/root-ca.csr -keyout root-ca/private/root-ca.key`
  - 根自签<br>
`# openssl ca -selfsign -config root.conf -in root-ca.csr -out root-ca.crt -extensions ca_ext`
此时会生成db/index文件，包含证书信息的明文，每行一个证书<br>
```
每行6项
1.状态标记 V有效,R吊销,E过期
2.过期时间YMDHMSZ格式
3.吊销日期 如果没有为空
4.序列号 16进制
5.文件路径
6.可分辨名称
```
  - 为CA生成CRL<br>
`# openssl ca -gencrl -config root.conf -out root-ca.crl`
  - 吊销证书<br>
使用revoke需要一个副本，不过如果证书都在一个位置。只用序列号就可以<br>
`openssl ca -config root.conf -revoke certs/xxx.pem -crl_reason xxx(crl_reason有几个规定的值)`
  - 生成用于给OCSP签名证书<br>
OCSP证书无法吊销，所以其生命周期要比较短
```
# openssl req -new -newkey rsa:2048 -subj "/C=CN/O=test/CN=OCSP Root Responder"\
 -keyout private/root-ocsp.key  -out root-ocsp.csr
# openssl ca -config root.conf -in root-ocsp.csr -out root-ocsp.crt \
-extensions ocsp_ext -days 30
```
**启动根CA的OCSP服务**<br>
`openssl ocsp -port 9080 -index db/index -rsigner root-ocsp.crt -rkey private/root-ocsp.key -CA root-ca.crt -text`
**验证证书是否吊销**<br>
`openssl ocsp -issuer root-ca.crt -CAfile root-ca.crt -cert root-ocsp.crt -url http://localhost:9080`
- 二级CA<br>
[地址](://github.com/ivanr/bulletproof-tls/blob/master/private-ca/sub-ca.conf)
  - 生成二级CA<br>
```
生成二级CA 的CSR
openssl req -new -config inter.conf -out sub-ca.cssr -keyout private/sub-ca.key
根证书签名
openssl ca -config root.conf   -in sub/sub-ca.cssr -out sub/sub-ca.crt -extensions sub_ca_ext
```
