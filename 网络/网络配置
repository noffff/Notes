有时候多块网卡时，默认路由是随机的。只要在网卡配置文件中加入 DEFROUTE=yes 参数，就会让该网卡成为默认路由。让其成为默认路由的时候，还可能存在一个问题。机器的DNS地址仍旧不是该网络的。因此需要加入PEERDNS=no参数让其dhcp的时候不修改/etc/resolve.conf文件。自己手动的修改该文件，把其DNS地址配置为自己想要的即可。
该网址是centos官方对网卡配置参数的解释
https://www.centos.org/docs/5/html/Deployment_Guide-en-US/s1-networkscripts-interfaces.html


加入几个网卡后，每个网卡默认都是dhcp方式，然后重启network服务时报错如下
Jun 12 02:29:53 my-op-1.novalocal network[2424]: RTNETLINK answers: File exists
查看进程发现有多个dhclient进程，怀疑是多个dhclient发生某文件冲突，将所有dhclient服务都杀掉以后，再次启动服务无报错。


修改网络相关的命令nmcli
创建桥
# nmcli con add type bridge ifname {Bridge-Name}
每个桥都有优先级，优先级值小的会被选作为root桥，可以在创建桥时指定优先级 {priority value} 默认32768 range范围 0-65535
查看已接入的网络设备
# nmcli con show 
对现有网络设备进行修改
# nmcli con modify  bridge-name 
使用nmcli创建网桥
# nmcli con add type bridge con-name xenbr0 ifname xenbr0
# nmcli con modify xenbr0 bridge.stp no
# nmcli con modify xenbr0 bridge.hello-time 0
将网卡连接到桥
# nmcli con modify "System eth0" connection.master xenbr0 connection.slave-type bridge



	
	
