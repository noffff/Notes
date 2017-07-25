# 套接字 socket
  - 建立在服务端的通信端点，用来接收连接请求的类似插孔的概念，是一种计算机网络数据结构。
```
在BSD套接字下分为面向文件和网络两种类型套接字。
每种类型的套接字对应不同的“家族名称”
例如IPV6寻址的地址家族为AF_INET6
Python支持的地址家族(socket_family)有
AF_NETLINK:无连接 允许用户级别和内核级别代码之间IPC(Inter Process Communication)
AF_UNIX:本地文件
AF_TIPC:集群中机器通信，不用IP寻址
AF_INET:因特网
```
- 面向文件套接字
  - 进程间通信，UNIX套接字 称为AF_UNIX/AF_LOCAL
- 面向网络套接字
  - AF_INET
** 主机+端口=套接字地址 **

- 套接字种类
  - 面向连接
    - 虚拟电路、流套接字 基于TCP的特性。使用TCP必须创建SOCK_STREAM套接字类型
  - 无连接
    - 数据报 基于UDP特性，使用SOCK_DGRAM

- Python调用socket()函数创建socket类型 socket(socket_family,socket_type,protocol=0)
  - TCP Socket为 socket(socket.AF_INET,socket.SOCK_STREAM)
  - UDP Socket为 socket(socket.AF_INET,socket.DGRAM)
## TCP server socket
通过调用python自带的socket实现。该socket为最基础的socket模块。
```
import socket
import time
ssss = ('::1',8888)
s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
s.bind(ssss)
s.listen(5)
while True:
    print('Please Waiting for connection')
    cs,address = s.accept()
    print(address)
    # print('the address is %s' % address)
    while True:
        data = cs.recv(1024).decode('utf-8')
        print(data)
        if not data:
            break
        Tm = time.ctime()
        cs.send(("[%s] %s"%(Tm,data)).encode('utf-8'))
```
## TCP Client socket
```
import socket
Add = ('::1',8888)
Cli = socket.socket(socket.AF_INET6)
Cli.connect(Add)
while True:
    data = 'The client send'
    if not data:
        break
    Cli.send(data.encode('utf-8'))
    data1 = Cli.recv(1024)
    if not data1:
        break
    print(data1.decode('utf-8'))
```
## UDP Server socket
```
import socket
import time
ADD = ('::1',9999)
udp_Socket = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
udp_Socket.bind(ADD)
while True:
    print('waitting for message')
    data,add = udp_Socket.recvfrom(1024)
    udp_Socket.sendto(('[%s] %s'%(time.ctime(),data)).encode('utf-8'),add)
    print('recvived from and returned to :',add)
```
## UDP Client socket
```
import socket
ADD = ('::1',9999)
udp_Client = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
while True:
    data = 'this is udp message'
    if not data:
        break
    udp_Client.sendto(data.encode('utf-8'),ADD)
    data,ADD = udp_Client.recvfrom(1024)
    if not data:
        break
    print(data.decode('utf-8'))
```
#socketserver
 该库集成了多个多样本网络编程模板，不必在进行繁琐的创建等工作。
#Twisted
完整的事件驱动框架，提供各类工具包


