## URL组成
- prot_sch
协议
- net_loc
服务器地址
- path
文件或CGI应用路径
- params
可选参数
- query
连接符`&`分隔的一系列key value对
- frag
指定文档内特定的部分

## 包
### urllib
整合了py2的urlib、urlparse、urllib2
常见几种打开网站的方式  
#### urllib.request.urlopen('xxx')  
该种方式文件的方式打开  
所以还需要`read`操作
### quote
转换为urlencode，使其可以用于URL字符串中。除此之外，有些不能转化的会在前面加上`%`后面转为十六进制
