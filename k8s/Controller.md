# 控制器
k8s内部包含多个高级的抽象工具---**Controller**。控制器是利用基础对象，提供了许多附加的功能和较为方便的特征  
## 种类
- [ReplicaSet](###ReplicaSet)
- Deployment
- StatefulSet
- DaemonSet
- Job
### ReplicaSet
ReplicaSet是新一代的副本控制器，用来保证pod的副本和在创建声明时的一致，与Replication Contronller唯一区别在于对`selector`的支持  
其支持新一套的`selector`  
大多数kubectl命令支持两种副本控制。只有rolling-update命令除外。如果想使用滚动升级的功能应该使用`Deployments`。  
ReplicaSet可以独立工作，但当今主流都是使用更高级的`Deployment`来进行pod的编排工作。Deployment自己会管理ReplicaSet  
[Example](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/concepts/workloads/controllers/frontend.yaml)

### Deployments
提供了对ReplicaSet和Pod的管理  
#### 用途
##### 创建Deployment
[例子](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/concepts/workloads/controllers/nginx-deployment.yaml)
> 在创建一个deployment时，可以使用`record`来记录这一次的操作。该记录与版本号对应  
创建完后可以使用`kubectl get deployments`来查看状态  
`kubectl rollout status deployment nginx-deployment`显示状态  
查看通过Deployment创建的ReplicaSet(rs)`kubectl get rs`  
查看自动生成的pod及标签`kubectl get pods --show-labels`
##### 升级Deployment
升级Pod模板的声明，然后创建一个新的ReplicaSet，Deployment会将Pod从老的ReplicaSet一到新的里面，每一次升级都会更新Deployment的版本号
当Deployment Template中的pod Template被改变(**只有仅且这项改变**)，就会触发`Deployment rollout`。  
可以通过`kubectl set`|`kubectl edit`来编辑资源进行修改  
###### Roll策略
升级时Deployment会先让一部分pod进行升级操作(至少一个pod是正常)(1 max unavailable)  
Deployment也会保证只有在原有希望pod数的基础上有一部分的Pod会被创建启动，默认是1个(1 max surge)  
在升级部署时，他不会杀掉老的pod，直到有足够数量新的pod启动之后。也不会一直创建新的pod，直到老的pod被杀掉。这就保证了服务的可用性。  
##### 回滚Deployment版本
可以取消当前的`rollout`--`kubectl rollout undo deployment nginx-deployment`  
也可以指定版本号回滚  
`kubectl rollout undo deployment nginx-deployment --to-revision=2`  
##### 调整规模
###### 调整副本数
`kubectl scale deployment nginx-deployment --replicas=x`
在打开**horizontal pod autoscaling **后，也可以根据根据每个pod使用的资源使用情况来设置自动调整  
除此之外，还可以暂停或者恢复Deployment。来进行一次大的调整。  


