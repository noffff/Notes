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

## 控制器
高级对象  
k8s内部包含多个高级的抽象工具---**Controller**，对基础对象进行了封装，从而提供高级并且便捷的功能  
### 种类
- [ReplicaSet](####ReplicaSet)
- [Deployment](####Deployments)
- [StatefulSet](####StatefulSet)
- [DaemonSet](####DaemonSet)
- [Job](###Job)

#### ReplicaSet
ReplicaSet是新一代的副本控制器，用来保证pod的副本和在创建声明时的一致，与Replication Contronller唯一区别在于对`selector`的支持  
其支持新一套的`selector`  
大多数kubectl命令支持两种副本控制。只有rolling-update命令除外。如果想使用滚动升级的功能应该使用`Deployments`。  
ReplicaSet可以独立工作，但当今主流都是使用更高级的`Deployment`来进行pod的编排工作。Deployment自己会管理ReplicaSet  
[Example](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/concepts/workloads/controllers/frontend.yaml)

#### Deployments
提供了对ReplicaSet和Pod的管理  
##### 用途
###### 创建Deployment
[例子](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/concepts/workloads/controllers/nginx-deployment.yaml)
> 在创建一个deployment时，可以使用`--record`来记录这一次的操作。该记录与版本号对应  
创建完后可以使用`kubectl get deployments`来查看状态  
`kubectl rollout status deployment nginx-deployment`显示状态  
查看通过Deployment创建的ReplicaSet(rs)`kubectl get rs`  
查看自动生成的pod及标签`kubectl get pods --show-labels`
###### 升级Deployment
升级Pod模板的声明，然后创建一个新的ReplicaSet，Deployment会将Pod从老的ReplicaSet一到新的里面，每一次升级都会更新Deployment的版本号
当Deployment Template中的pod Template被改变(**只有仅且这项改变**)，就会触发`Deployment rollout`。  
可以通过`kubectl set`|`kubectl edit`来编辑资源进行修改  
如改变镜像`kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1`  
###### Roll策略
升级时Deployment会先让一部分pod进行升级操作(至少一个pod是正常)(1 max unavailable)  
Deployment也会在原有期望的pod数的基础上在额外创建一部分的Pod，默认是1个(1 max surge)  
在升级部署时，他不会杀掉老的pod，直到有足够数量新的pod启动之后。也不会一直创建新的pod，直到老的pod被杀掉。这就保证了服务的可用性。  
###### 回滚Deployment版本
可以取消当前的`rollout`--`kubectl rollout undo deployment nginx-deployment`  
也可以指定版本号回滚  
`kubectl rollout undo deployment nginx-deployment --to-revision=2`  
###### 调整规模
###### 调整副本数
`kubectl scale deployment nginx-deployment --replicas=x`
除此之外，还可以暂停或者恢复Deployment。来进行一次大的调整。  
###### pod的自动扩展
在开启**horizontal pod autoscaling**功能后，可以设定pod数量的范围（最小和最大）。然后可以基于CPU的利用率来使其自动扩展
`kubectl autoscale deployment nginx-deployment --min=1 --max=2 --cpu-percent=60`  

#### StatefulSets
用来管理有状态的应用。1.8beta 

#### DeamonSet
一个DaemonSet管理一些node运行一个pod的副本。当节点从集群中移除时，pod也会被视为垃圾回收。删除一个daemonSet，pod也会被移除  

# 技巧
## 选择特定的node运行pod
为node加上标签`kubectl label nodes --all test=test1`  
然后利用`nodeSelector`按照label选取  
```
      nodeSelector:
       test: test1
```
