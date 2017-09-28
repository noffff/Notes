# 对象
## 基础对象
### Pod
Pod在k8s中是最小的可部署对象模型,k8s可以部署用户创建的Pod从而在集群中产生相应的进程  
Pod可以运行在一个或多个容器中，其可能包括存储资源、IP。在k8s中是一个独立的实例  
一般情况下，k8s中Docker是Pod最为普遍的运行体现。  

#### 工作方式
- Pod运行单个容器
- Pod运行多个容器
运行多个容器时是紧密耦合的，他们共享资源。  
一个Pod中的多个容器相互之间沟通的网络是**localhost**。它们共享Network namespace及ip地址、端口  
一个Pod可以指定一系列的共享存储卷。在一个Pod中的所有容器能够访问共享存储，从而使这些容器可以共享数据。  

#### 工作情形
Pod是**最小的工作单位**，这个意思就是就算重启也只应该重启Pod而不是重启容器。并且与Pod相对应的进程如果执行完毕  
Pod就会删除。其生命周期非常短暂。在资源紧张或者Node维护时就会挂掉。结合这些信息来看，一般不会直接进行Pod的操作，可以使用`Controller`来创建管理Pod。

#### Controller
一个`Controller`可以创建和管理多个Pod。并且拥有处理副本及自我恢复能力(故障疏散)  
通常情况下，Controller是按照用户提供的Pod Template来工作的

#### Pod Template
所谓模板就是一个Pod的描述，描述其组成、声明其用到的资源。比如`ReplicateControllers`、`jobs`、`DaemonSet`。  
模板被利用生成后，就与该工作再也没关系

### Service
Pod终有一死(mortal)，不能复活。除此之外，Pod的IP在整个时间内也是不稳定的。那么一组做后端的Pod和一组前端的Pod是如何相互定位的  
这时候就需要叫做`Service`的功能  
k8s中的`Service`用来定义一组逻辑的`Pod`以及它们之间的访问策略。`Service`涵盖的Pod由`Label Selector`决定  
这样后端变化时，前端根本不管只是会以`Service`为目标进行连接  
在k8s的原原生应用中，k8s提供简单的API接口来更新Service中的Pod。对于不是原生的应用，K8s提供虚拟IP可以桥接在后端Pod上  

