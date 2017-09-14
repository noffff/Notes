# 概念
## 内存架构
### 32位内存结构区域
- ZONE_DMA(0-16MB)
- ZONE_NORMAL(16MB-1GB)
  - 保留区域(896MB-1GB)
  用于映射ZONE_HIGHMEM的地址  
- ZONE_HIGHMEM(1GB-64GB)  
### 64位内存结构区域
- ZONE_DMA(0-1GB)
- ZONE_NORMAL(1GB-64GB)
## 内存管理
为了提高内存的管理，目前系统使用`分页(page)`技术对内存进行管理
分页将内存划分为固定的chunk，分页的大小由CPU架构决定，一般x86和i386为4KB
物理内存被分成`页帧(page frame)`。一个页帧包含数据的一个分页
进程不能直接对物理内存寻址，为一个进程分配内存时会将页帧的物理地址映射到进程的地址空间，表现为虚拟的地址(每个进程都有地址空间)
进程只能访问自己的私有地址空间，虚拟空间大小由CPU架构决定。但是进程不会一次性的占用所有地址空间(物理地址未映射，未分配)。
32位地址空间2^32B(4G),其中用户空间区域为**0-3G**，内核空间区域**3G-4G**
64为地址空间2^64B(16EB),用户空间和内核空间无限制  
### 页状态
- Free 
有效分页，可立即被分配
- Inactive Clean
不活跃分页，已分配给进程，但最近没有调用
- Inactive Dirty
不活跃的脏页,等待将数据输入磁盘
- Active
活跃的分页，已分配给进程，最近刚使用  
### 页的分配
一个分页是页帧或虚拟内存的一个线性地址。内核以内存页为单位处理内存
当进程请求一定数量的内存页时，如果剩余内存量充分，将会立刻分配。否则会从其它程序或分页缓存中得到。
### 页的回收
当请求到来，却没有有效分页时。内核将释放一定数量的页(之前使用，但目前因为某些原因被标记为不活跃的页)，然后将这些页分配给请求的进程。  
通过内核线程`kswapd`和内核函数`try_to_free_page()`进行上述的分页回收。  
如果因为(过量使用内存)[###内存过量使用]不能及时回收会出现`Out-of-Memort,OOM`错误。其它的内存管理工具都已经失效时，会通过`OOM killer`选择杀死进程来释放内存直到系统稳定。  
OOM killer每个进程的`oom_score`分数来杀，越高越杀   
Linux中管理OOM killer的文件有三个
- /proc/PID/oom_adj
已经不用  
- /proc/PID/oom_score  
- /proc/PID/oom_score_adj
用户可以使用该值来控制oom_killer的过程, 而不使用`oom_adj`  
取值范围从-1000到1000。-1000永不杀  
`kswapd`线程平时处于可中断睡眠状态，当区域空闲分页少于一个阈值，会被激活。基于`最近最少(Least Recently Used LRU)`原则释放分页。  
一般`Anonymous Page`不会轻易释放，释放还需要将其从磁盘拿到内存中进行。  
关于将脏数据刷入磁盘的相关控制参数  
- vm.dirty_expire_centisecs
脏数据多久后才能写入磁盘，单位百分之一秒
- vm.dirty_writeback_centisecs
内核多长时间唤醒flush线程进行一次数据写入，0为禁止周期写入
- vm.dirty_background_ratio
脏数据占系统内存百分比达多少时，内核开始后台写出数据到磁盘
- vm.dirty_ratio
进程所拥有的脏数据占用系统内存的百分比的阈值，超过该阈值进程产生写阻塞，写出脏页
> 除此之外还能对脏数据的字节数设置阈值，具体参数可以sysctl -a|grep dirty查看  
### 虚拟内存管理
对于进程来说，其调用的都是内核映射给他们的虚拟内存，因此进程并不知道虚拟内存至下到底是真正的内存还是来自磁盘的`swap虚拟内存(匿名分页)`  
kswapd扫描活跃分页的列表，将最近没使用过的放入非活跃分页列表。  
分页回收发生时，非活跃列表中的`进程地址空间`的候选分页会被`page out`。  
有时，page out操作只是为了保证主内存的分配。比如内存分页已经用完，但是某进程时间片还有很多，就会将其进行page out  
所以swap较高也不一定是性能不足，只是为了更好的利用系统资源  
`vmstat -a`显示活跃和分活跃分页数
除此之外，kswapd回收分页时宁可缩小分页缓存大小也不愿意对进程分页进行`page out`或`swap out`操作  
- page out
将地址空间的一部分分页移动到swap中
- swap out
将整个地址空间放入swap  
> kswapd 回收分页缓存或者回收进程地址空间会根据不同场景来进行。具体可以使用/proc/sys/vm/swappiness来控制  
进行计算是swap还是out时有三个值对齐造成影响
- distress
最大值是100，内核请求释放内存次数，第一次请求为0，随后逐渐递增  
- mapped_ratio
该值单位是一个百分比，近似等于系统在一个地址空间中内存映射的比例。
- vm_swappiness
该值的大小起到一个权重的作用，能够影响对回收分页时使用`out`操作还是`drop page cache`操作   
取值范围为`0-100`,值越低越偏向drop，越高越偏向out操作  
根据以下计算公式，从而得到`swap_tendency`  
	swap_tendency = mapped_radio / 2 + distress + vm_swappiness  
swap_tendency =< 100时，内核会回收利用`page cache`  
swap_tendency > 100 时，进程地址空间中的page也会被回收利用  
假设`distress`值非常小，`vm_swapiness`值为60，只有在系统内存被分配出去`80%`之后，才会考虑`swap/page out`操作  
可以根据不同的应用环境，来进行对该值的调整,也可以使用cgroups来为不同的应用设置  
[参考链接](https://access.redhat.com/solutions/103833)
### Buddy System
维护内存分页，将较小临近的分页合并为一个较大的分页  
`cat /proc/buddyinfo`可以查看buddy的相关状态信息
### 内存过量使用
Linux支持过量使用  
通过改变`/proc/sys/vm/overcommit_memory`的值来开启，其值有如下几个  
值|意义|
----|----|
0|内核会估计请求内存后所剩余的内存是否充裕，默认为0|
1|内核会假装内存始终是充足的，直到真正耗尽|
2|内核从不过量使用内存，会阻止所有过量使用的内存|  
这个特征是很有用的，因为有许多进程都会`malloc`很多，但实际用不到。分配的虚拟内存，并不保证真实存在物理存储设备上  
该机制提高了利用效率，但是当正好需要该虚拟分配的内存，而内核找不到有效的分页时 那就GG了。  
### TLB
进程的内存都是从物理内存映射到进程地址空间的虚拟内存。因此需要有一张表来记录虚拟内存与物理内存的映射关系  
每个page在表上都占一项，但进程使用的内存越多这个映射表就会越大。在查表时就会有更大的开销。  
为了加快这个过程，会将其缓存在`Translation Looksaide Buffer,TLB`，CPU的旁路转换缓存。  
内核调度进程，就会刷新一次TLB  
越大的分页，其对应的TLB映射空间也会越大。越难命中，反之亦然  
### 透明的巨型分页
Linux 6.2开始引入，默认开启  
内核动态创建调整，无需人工接入  
`/sys/kernel/mm/transparent_hugepage/enabled Always/madvise开启 never关闭 控制khugepaged的自启动`
`/sys/kernel/mm/transparent_hugepage/defrag 控制内核是否积极使用压缩内存大页`
### 内存页合并
`Kernel Samepage Merging,KSM`从名字就能看出其用来合并相同的page，用来作为shared  
KSM分为两个服务  
- ksm
实际扫描内存和合并内存分页
- ksmtuned
控制ksm是否扫描内存和定义如何扫描内存  
