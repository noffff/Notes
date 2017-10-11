# 环境准备
## 关闭Selinux
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
## 清除防火墙
iptables -F
iptables-save > /etc/sysconfig/iptables
## 设置防火墙规则
- 打开宿主机的22端口
iptables -I INPUT -p tcp -m state --state NEW,RELATED,ESTABLISHED -m tcp --dport 22 -j ACCEPT
- 打开防火墙相应的连接通道
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
- 打开DHCP端口
iptables -A INPUT -p udp -m multiport --dports 67,68 -j ACCEPT
- 打开DNS端口
iptables -A INPUT -p udp --dport 53 -j ACCEPT
- 设置防火墙默认策略
iptables -P INPUT DROP
- 保存策略
iptables-save > /etc/sysconfig/iptables
## 安装epel源
yum -y install epel-release
## 检测是否支持虚拟化
lscpu |grep -E '(vmx|svm)'
## 检测是否加载kvm模块
lsmod|grep kvm
# 安装软件及创建
## 安装相对应软件
yum -y install libvirt qemu-kvm libvirt-client virt-install bridge-utils
## 开启libvirtd
systemctl enable libvirtd.service  
systemctl start libvirtd.service  
## kvm网络
kvm会默认创建一个**defalut**网络和一个虚拟网卡,vm如果不指定网络方式会对该网卡进行nat方式上网，使用下列命令进行操作  
- 查看网络
virsh net-list
- 查看默认网络信息
virsh net-info defalut
- 查看该网络详情
virsh net-dumpxml default
## 设置防火墙规则让vm上网
如果没有这一步，默认情况创建出来的vm是不能上网的，要利用[kvm](##kvm网络)从网络信息中得出将要创建出来vm的地址段，这里我是192.168.122.0/24段  
因此使用iptables nat方法将该网段内容进行POSTROUTING转发操作  
iptables -t nat -A POSTROUTING -s 192.168.122.0/255.255.255.0 -o em1 -j MASQUERADE  
操作完毕记得`iptables-save > /etc/sysconfig/iptables`
## 创建硬盘
qemu-img create -f raw -o size=20G Centos7_base_raw.img
## 创建vm
```
virt-install --name Cen7_base_raw --ram 2000 --vcpus 2 \
--disk /vm_image/disk/Centos7_base_raw.img\
 --cdrom vm_image/iso/CentOS-7-x86_64-Minimal-1708.iso\
 --graphics type=vnc,listen=0.0.0.0  
```
至此该VM已经创建完毕，要使用VncClient连入宿主机的5900端口进行手动的安装操作
