[本文翻译自](http://bencane.com/2012/08/06/troubleshooting-high-io-wait-in-linux/)
## 检测是否因为IO原因导致系统变慢
可以使用`top`等检测**wa**的值，如果该值较高，表明较多的CPU资源在等待IO操作  
- wa(iowait)
cpu花费到等待IO完成的时间片数
## 检测哪个存储设备正在被写入  
如果发现该值较高时，可以通过`iostat`来查找系统所有的IO情况  
这里要使用`iostat -xy`，`-x参数能够显示拓展信息，帮助判断  
查看命令的输出的`%util`值表示设备的利用率  
## 找出造成高IO的进程
可以使用`iotop`，如果该命令没被安装可以使用`ps -eo state,pid,cmd|grep ^D`查看哪个进程是出于后端调用IO操作的  
当然，不一定处于`uninterruptible sleep(D)`阶段就是元凶，还需要查看其IO的情况  
这里，我们根据得到的PID查看`/proc/PID/io`查看其io信息  
```
rchar: 72265897
wchar: 61970967
syscr: 510868
syscw: 37780
read_bytes: 92286976
write_bytes: 99938304
cancelled_write_bytes: 0
```  
然后根据`read_bytes`和`write_bytes`字段分析  
## 找出进程IO过重的文件
`lsof -p PID`
