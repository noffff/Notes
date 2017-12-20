# k8s
**k8s分为master和node两大部分，master起调度配置作用，不工作，而node承担工作任务**  
## Master组件
### kube-apiserver
暴露k8s的API
### etcd
一个分布式存储，类似于redis的存在。
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
### kubelet(必备)
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
### docker/rkt(必备)
