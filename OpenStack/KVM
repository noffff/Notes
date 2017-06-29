KVM可以指定磁盘的缓存模式。
	1.writethrough
	2.writeback
	3.none
	4.directsync
	7.unsafe
使用缓存可能在某些特定时候，导致数据的丢失。

QEMU支持磁盘镜像格式：
	1.raw
	2.qcow2
	3.cow
	4.qcow2
	5.vmdk
	6.dmg Mac磁盘格式
raw格式是一次性分配完空间，而qcow2则用多少分配多少。但在支持稀疏特性的文件系统中 ls raw格式 是已分配的大小，du raw格式 会显示很小，没有分配的大小。
raw和qcow2镜像可以作为后备镜像。差量镜像只能是qcow2。(raw和qcow2可以作为后端镜像，而qcow2可以作为前端的镜像。)
qcow2可以做快照。


虚拟上网有两种方式，桥接和nat方式。
在宿主机中以Linux-Bridge的形式，将所有虚机的虚拟网卡接入到这个桥里。
如果使用桥接方式，需要将一块物理网卡加入到这个桥里。
如果使用nat方式，则不需要将物理网卡加入桥里，将这个桥的流量通过iptables 进行SNAT，使桥中的虚机网卡能够上网。
docker上网方式也类似。

有很多种创建虚机的方式，可以使用virsh 通过已经定义好的XML文件创建。也可以通过virt-install 指定虚拟机使用的资源（内存，VCPU等）来创建，该方法创建的虚拟机会默认生成XML文件

对KVM虚机CPU调优可以是有 numactl 这个包
KVM虚机CPU架构为NUMA，可以使用“virsh numatune 虚机ID”查看虚机CPU NUMA的架构类型，一般有strict(指定CPU)和auto(使用系统numad服务)
每个虚拟机上的核都会对应物理机上的一个核，可以通过 "virsh vcpuinfo instance-name/instance-number"
http://orh0ftvwf.bkt.clouddn.com/%E6%8A%A5%E5%A4%B4%E7%BB%93%E6%9E%84.jpg
如图中所示，虚拟核0 调度到宿主机核3上。而其中的y表示虚拟核可以被调度到那几个物理核
CPU绑定通过Cgroup实现。，也可以通过Cgroup直接绑定KVM虚拟机的进程也可以。
设定VCPU的最大值，然后当前VCPU小于这个值时，可以使用模拟热插拔的技术增加 #VCPU setvcpus 虚机 VPU_COUNT --live 在线  qemu必须在1.5之上。CentOS7系统
目前不支持热拔/热减少VCPU 不过可以关闭VCPU。/sys/devices/system/cpu/cpuN/online  将该值设为0，表明N号CPU不工作

KVM在使用VCPU时，默认情况不会准确显示物理CPU的型号，因此也不具备物理CPU的一些特性，在某些情况下是需要物理CPU的特性的，可以将cpu mode设置为 'host-passthrough'。使用该方式时，不同型号CPU的宿主机之间虚拟机不能迁移。
下面为默认的cpu模式，
" 
<cpu mode='custom' match='exact'>
    <model fallback='allow'>Westmere</model>
</cpu>
"
指定"host-passthrough"模式
"
<cpu mode='host-passthrough'/>
"
禁止一些虚机被主机进行KSM，
<memoryBacking>
	<nosharepages/>
</memoryBacking>
KVM 内存气球：
	所谓气球，就是可膨胀可缩小。内存气球意思就是KVM虚机内存动态改变，不过要依赖于 “virt balloon”和“内核开启 CONFIG_VRITIO_BALLOON” CentOS7默认已经做了所有工作
	虚拟配置文件中需要加入
	"
	<memballoon model='virtio'>
		<alias name='balloon0'/>
	</memballoon>
	"
	在虚拟机的lspci可以看到“ Red Hat, Inc Virtio memory balloon”这样的设备