# 套接字 socket
建立在服务端的通信端点，用来接收连接请求的类似插孔的概念，是一种计算机网络数据结构。<br>
** 主机+端口=套接字地址 **

## 套接字种类
在BSD套接字下分为面向文件和网络两种类型套接字,每种类型的套接字对应不同的“家族名称”<br>
- 套接字种类
  - 面向连接
    - 虚拟电路、流套接字 基于TCP的特性。使用TCP必须创建SOCK_STREAM套接字类型
  - 无连接
    - 数据报 基于UDP特性，使用SOCK_DGRAM

- 面向文件套接字
  - 进程间通信，UNIX套接字 称为AF_UNIX/AF_LOCAL
- 面向网络套接字
  - AF_INET

- Python支持的地址家族(socket_family)
  - AF_NETLINK:无连接 允许用户级别和内核级别代码之间IPC(Inter Process Communication)
  - AF_UNIX:本地文件
  - AF_TIPC:集群中机器通信，不用IP寻址
  - AF_INET:因特网

## 使用方法
Python调用socket()函数创建socket类型,其格式如下:<br>
`socket(socket_family,socket_type,protocol=0)`<br>
- TCP 类型Socket
  socket(socket.AF_INET,socket.SOCK_STREAM)
- UDP 类型Socket
  socket(socket.AF_INET,socket.DGRAM)

## 库
- socket
  最基础的socket模块。
- socketserver
  该库集成了多个多样本网络编程模板，不必在进行繁琐的创建等工作。
- Twisted
  完整的事件驱动框架，提供各类工具包


