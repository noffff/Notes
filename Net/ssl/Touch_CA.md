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
`openssl ocsp -port 9080 -index db/index -rsigner root-ocsp.crt -rkey private/root-ocsp.key -CA root-ca.crt -text`<br>
> openssl ocsp sever只是测试的程序，**only useful for test and demonstration purposes**,一次只能支持一次查询。当出现Invalid request 
Reply Error: malformedRequest (1)时表明可能请求方法不对。其不支持GET


**验证证书是否吊销**<br>
`openssl ocsp -issuer root-ca.crt -CAfile root-ca.crt -cert root-ocsp.crt -url http://localhost:9080`<br>
> OCSP响应验证需要完整的证书链，-CAfile指定 
- 二级CA<br>
[地址](://github.com/ivanr/bulletproof-tls/blob/master/private-ca/sub-ca.conf)
  - 生成二级CA<br>
```
生成二级CA 的CSR
openssl req -new -config inter.conf -out sub-ca.cssr -keyout private/sub-ca.key
根证书签名
openssl ca -config root.conf   -in sub/sub-ca.cssr -out sub/sub-ca.crt -extensions sub_ca_ext
```
