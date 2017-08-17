# PKI public key infrastructure
是一套证书策略管理架构。用来创建、存储和分发数字证书。这些数字证书被用来确认公钥是否来自一个已经确信的实体。PKI将公钥映射到这些数字证书中，存储在源中心。
PKI会将把结构组织与公钥绑定。绑定是通过**CA**系统来完成的。CA是证书颁发系统，包含注册和颁发证书为一体。
PKI的用来保证正确注册的组织叫做**RA**.RA负责接收对于数字证书的请求并对认证请求作出回应。
在
每一个证书实体的CA域必须是独一无二的。第三方**VA**提供的实体信息可以代替CA
VA提供用来确认数字证书是否满足X.509和RFC 5280标准的每一个机制
- CRL 证书吊销列表
CA证书时包括了一个公钥,对应于每一个服务私钥。
CA证书的数字签名通常来自于一个可以的第三方机构。
游览器只有一个leaf 证书(针对服务的证书)通常是不够的，因为游览器是不知道其中间的证书，因此需要子证书包含这些。这一系列证书在游览器中叫证书bundle。
- 签发流程
  - 将用户身份信息、用户公钥信息。按照特定格式组成数据D
  - 用摘要算法对数据D进行计算得到摘要H
  - 使用CA私钥对摘要H进行加密得到数字签名S
  - 将用户信息、用户公钥信息、数字签名S按照特定格式组合成数字证书
## PKI组成
- CA
`存储、分发、标记数字证书`
- 注册认证，用来确认要将数字证书存在CA的实体。
- 中心目录，安全，存放信息的地方
- 证书管理系统
- 证书策略




## 根证书
最基本的证书，包含两部分
  - ca.key.pem 根秘钥
  - ca.cert.pem 根证书
上述这一对构成CA。
根证书通过自己的私钥自签。<br>
通常情况下，根CA不会直接对服务或客户端证书打标签。根CA证书经常用来生成中间级的CA。<br>这些中间级的证书会代替根CA来认证下级服务。这样子root-key可以离线的方式进行操作，保证了安全。<br>
创建根证书时必须要有一个能让OpenSSL使用的配置文件。
(配置文件介绍)[https://jamielinux.com/docs/openssl-certificate-authority/create-the-root-pair.html]
配置文件结构如下
- [ ca ]
> 指定使用的块参数
- [ CA_default ]
> 包含一系列的默认设置
- [ policy_strict ]
> 根证书的签发中间CA证书策略
- [ policy_loose ]
> 中间CA向下签发证书策略
- [ req ]
> 应用于创建证书或者证书签名的请求
- [ req_distinguished_name ]
> 声明证书签发请求中经常用到的信息
- [ v3_ca ]
> 在创建根证书时会用到的信息
- [ v3_intermediate_ca ]
> 在创建中间证书时会用到的
- [ usr_cert ]
> 签发客户端证书时用到
- [ server_cert ]
> 签发服务端证书时用到
- [ crl_ext ]
> 创建证书吊销列表时用到
- [ ocsp ]
> 签发OCSP**Online Certificate Status Protocol**证书时会用到
- 创建流程
  - root证书
    - root-key
`openssl genrsa -aes256 -out private/ca.key.pem 4096`
`chmod 400 private/ca.key.pem`
    - root-cert
```
openssl req -config openssl.cnf \
      -key private/ca.key.pem \
      -new -x509 -days 7300 -sha256 -extensions v3_ca \
      -out certs/ca.cert.pem
chmod 444 certs/ca.cert.pem
```
## 中间证书
- intermediate-key
`openssl genrsa -aes256 -out private/ca.key.pem 4096`
- intermediate-cert
生成CSR**请求签名证书**。其中信息要与根CA一致，CN段不同。
```
openssl req -config intermediate/openssl.cnf -new -sha256 \
      -key intermediate/private/intermediate.key.pem \
      -out intermediate/csr/intermediate.csr.pem
```
- 使用根证书对中间CSR进行签名认证
```
openssl ca -config openssl.cnf -extensions v3_intermediate_ca \
      -days 3650 -notext -md sha256 \
      -in intermediate/csr/intermediate.csr.pem \
      -out intermediate/certs/intermediate.cert.pem
chmod 444 intermediate/certs/intermediate.cert.pem
```
- 查询
`openssl x509 -noout -text -in certs/ca.cert.pem`
输出结构如下
```
Signature Algorithem:签名所用算法
Issuer:签名证书的实体
Validity:有效期
Public-Key:公钥长度
Subject:参考证书本身
Subject 和Issuer是根证书自签用
```
中间CA签发应用后，应用还会向根证书确认中间证书，而应用证书不知道根证书在哪，所以需创建一个包含根证书的CA证书链
```
cat intermediate/certs/intermediate.cert.pem \
      certs/ca.cert.pem > intermediate/certs/ca-chain.cert.pem
chmod 444 intermediate/certs/ca-chain.cert.pem
```
- 使用根证书验证中间CA
```
# openssl verify -CAfile certs/ca.cert.pem \
      intermediate/certs/intermediate.cert.pem
```
## 签发服务和客户端证书
这一块需要完成上面的根和中间CA的认证，自己作为颁发机构。<br>
而使用第三方的中间CA,就不会暴露它们的自己的私钥，他们给你CSR，你自己签获得签名证书。就直接跳过了genrsa和req命令。
使用中间CA来签发证书。这些签发的证书可以用于多种情况如web server，CS两端的安全连接等
客户端key字节数不能大于根和中间CA
而且key的加密长度越大，TLS握手会越慢。一般对于服务和客户端的key都用2048位
**If you’re creating a cryptographic pair for use with a web server (eg, Apache), you’ll need to enter this password every time you restart the web server. You may want to omit the -aes256 option to create a key without a password.**
- 创建key
```
# openssl genrsa -aes256 \
      -out intermediate/private/www.example.com.key.pem 2048
# chmod 400 intermediate/private/www.example.com.key.pem
```
- 创建CSR证书
使用私钥创建**证书签发请求**(CSR)**<br>该证书的CA信息可以与中间CA的不同。对于**服务端证书**来说，Common Name必须是服务的全域名<br>“in order for a browser to trust an SSL Certificate, and establish an SSL/TLS session without security warnings, the SSL Certificate must contain the domain name of website using it”。<br>对于**客户端证书**其可以是任一独立的值。Common Name不能与根或中间证书一样
```
openssl req -config intermediate/openssl.cnf \
      -key intermediate/private/www.example.com.key.pem \
      -new -sha256 -out intermediate/csr/www.example.com.csr.pem
chmod 444 intermediate/certs/www.example.com.cert.pem
```
- 使用中间CA来签名该CSR
```
# openssl ca -config intermediate/openssl.cnf \
      -extensions server_cert -days 375 -notext -md sha256 \
      -in intermediate/csr/www.example.com.csr.pem \
      -out intermediate/certs/www.example.com.cert.pem
# chmod 444 intermediate/certs/www.example.com.cert.pem
```
- 使用CA链来验证新证书
```
openssl verify -CAfile intermediate/certs/ca-chain.cert.pem \
      intermediate/certs/www.example.com.cert.pem
```
- 部署
部署时要确保三个文件有效
  - ca-chain.cert.pem
  - www.example.com.key.pem
  - www.example.com.cert.pem
如果签名的CSR来自第三方，那么是不能访问key文件的。所以你只能把`ca-chain.cert.pem和www.example.com.cert.pem`给这个机构
# X.509
定义了公钥证书的形式。被用于许多互联网协议，如HTTPS的基础协议TLS/SSL。<br>
X509证书包含一个公钥、一个身份信息（主机名、组织名、个体名）。也可以使用CA签名或者自己签名。<br>
可以利用该证书包含的公钥域使用相应私钥处理过的文档和第三方进行安全通信。<br>
除了规定证书的形式外，X.509也指定了在CRL**证书吊销列表**的相关信息，用来认证哪些证书作废。
- CA bundle
```一个包含了根和中间证书的文件。域证书加上CA bundle构成证书链,这个链用来提高证书与web游览器的兼容性，用来减少通过游览器或其他Client端访识别证书时而引起的安全警告```

## CA
游览器、操作系统、移动设备认证的授权的CA成员项目，一个CA机构必须符合复杂的详细的标准才能成为一员。一旦成为了一名合法的CA机构就可以颁发被游览器信赖的SSL证书。目前有较少的合法的CA机构。CA的过程越长，也就有越多的游览器和设备信赖其CA分发。证书必须有向后的兼容性比如老的游览器和移动设备。
游览器和设备会通过存储**根证书**来信赖一个CA。一般在游览器和设备安装之前会预装一部分CA库。
CA使用这些预装的根证书来颁发中间根证书(Intermediate CA)和终端数字证书。CA收到一个证书请求，验证应用程序，颁发证书并且发布颁发证书的有效状态。

