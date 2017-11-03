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

## 迁移pod
双节点，每个节点都有一个pod，一节点故障，该节点pod会迁移到另外节点，恢复正常pod不恢复时  
`delete pod xxxx` 默认grace-period为30秒，然后会在另外节点生成新的pod  
