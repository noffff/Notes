## Node
节点是k8s中的实际工作者，每个节点都能够运行pods并且被master节点所管理。  
Node 状态包含了以下信息  
- Address
这个字段的的情况取决于宿主机的设置  
  - Hostname
可以使用`--hostname-override`参数覆盖
  - Externalip
集群外部访问的ip
  - internalip
集群内部访问的ip
- condition
所有`runing`状态的节点都会有该字段
  - OutOfDisk 为True时表明节点空间不够在加入新`pod`,否则为False
  - Ready 为True时表明节点是健康的能够接受新的pod。False不健康不能接受，Unknown表示上次收到节点的信息为40s前
  - MemoryPressure 为True表明节点内存有压力
  - DiskPressure True表示磁盘是有压力的，容量较低
  - NetworkUnavailable 为True时表示节点网络配置不正确
- capacity
描述该节点的可用资源大小
- info
关于节点的描述信息，如内核版本、k8s版本等

https://kubernetes.io/docs/concepts/architecture/nodes/
