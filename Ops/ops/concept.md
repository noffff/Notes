# 概念
(参考链接)[https://unix.stackexchange.com/a/78766/229648]  
在Linux结构中，有两个空间
- 用户空间
- 内核空间
用户空间和内核空间中间有一个C库`glibc`，内核空间和用户空间通过这个库提供的系统调用接口实现了连接。  
![Linux架构图](https://i.stack.imgur.com/KvVwy.png)
## 内核空间可以被深度分为三层  
- 系统调用接口
- 独立架构的内核代码
- 依赖架构的代码  
`独立架构的内核代码`由几个逻辑单元组成如
- 虚拟文件系统(VFS)
- 虚拟内存管理(VMM)
- 等待
![内核的子系统图](https://i.stack.imgur.com/CzYmy.png)


