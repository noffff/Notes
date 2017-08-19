# CPU
## steal time
> steal time是VCPU等待真正CPU处理其他虚拟化进程的时间百分比
- 定义
vm在独立的主机中的虚拟化环境中与其它实例分享资源，其中就包括CPU使用周期，如果主机上有四个相同规模的VM，那么其中任一个不能占用超过所有CPU周期的25%(k可以允许超过)
如果steal time超过规定的阈值，会关掉vm并在其他物理server上启动。环境上如果有虚拟化环境，steal time占用较高会严重影响极其性能。
steal过高两种情况：
每个VCPU steal 过高，提升VM CPU的资源
只有一个CPU过高，迁移VM到其他主机
