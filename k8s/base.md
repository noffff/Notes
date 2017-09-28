# k8s
## Master组件
### kube-apiserver
暴露k8s的API
### etcd
k8s的后端存储，所有集群的数据都会存在该出。一个分布式存储
### kube-controller-manager
控制组件，控制集群中处理日常任务的后端线程。
- node controller
责节点关闭时的一些事情
- replication controller
负责维护系统中每个副本控制对象的维护的pod数的正确性
- endpoint controller
控制端点
- Service account和token controller
微信的命名空间创建默认用户和访问API的token
### kube-scheduler
监控新创建并且没有分配node的pod，为其分配一个node。调度器。
### addons
addons是实现pods和service集群的手段、 

## Node组件
### kubelet
是主节点的agent，监控并对已经分配给节点的pod
- 为pods挂载卷
- 下载pod的secret
- 使用容器运行pods
- 周期性检测容器健康状况
- 向系统汇报pod/node的状态
### kube-proxy
在主机上维护一些规则，转发一些链接请求。
### fluentd
记录集群日志

## k8s对象
### 概念
对于k8s的对象操作，如创建、修改、删除的操作都是通过k8s API。`kubectl就是命令行的接口，当然也可以在项目中直接调用k8s API   
k8s的对象是用来反映集群的状态。一个对象对应用户的一个目的实体。k8s系统会不断检测该对象的存在，用户定义的对象会告诉k8s，集群应该是什么样的，是一个服务的期望状态  
每个K8S对象包括两个`nested`字段，一个是对象的**声明**，一个是对象的**状态**  
声明描述对象的期望状态，状态描述了当前对象的状态。  
对象被k8s使用和更新，k8s使状态描述字段与声明描述字段变的一致  
### 创建对象
创建对象时，必须提供对象的声明字段内容。一般情况，使用`kubectl`调用创建时，会提供一个`yaml`文件。`kubectl`会将该文件内容转换为JSON发送给API  
```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```
#### 必须的字段
- apiVersion
指定使用的API版本
- kind
创建什么种类的对象
- metadata
该类包含一系列的字段，用来作为区分对象的信息如**name**,**UID**,以及**namespace**
- spec
表明每个对象的不同
在K8s的API中，所有对象都有独一无二的名称或UID。名称由Client给予，UID由k8s生成  
在一个物理的k8s集群之上，可以创建多个虚拟的k8s集群，这些虚拟集群叫做`namespace`  

## Node
节点是k8s中的工人，每个节点都能够运行pods并且被master节点所管理。  
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
所有`runing`状态的节点都会有该字段，表明当前节点的所处条件如**磁盘满**,**内存满**
- capacity
描述该节点的可用资源大小
- info
关于节点的描述信息，如内核版本、k8s版本等
## 节点的管理

