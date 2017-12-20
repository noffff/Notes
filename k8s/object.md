# k8s对象
## 对象的意义
对于对象的操作(如创建、修改、删除)都是通过k8s API。可以使用`kubectl`，或者直接调用k8s API   
对象是持久化在k8s系统的实体，通过使用这些对象来表现集群的状态。通常是以下三种类型  
- 正在运行的应用
- 应用所涉及的资源
- 应用的策略行为，如重启策略、升级策略、容错率  

用户通过声明对象，来表示自己的意图如应用的规模、集群的结构等等。一旦创建了对象，那么k8s系统就会开始工作已确保对象存在。  
用户声明的对象，是对服务状态的一种理想化描述。而服务本身还会受到各种因素的影响。因此每个k8s的对象自己还包含两个对象字段  
一个字段叫做`spec`，就是存储用户描述的理想状态。而另外一个字段`status`，就是对象的当前状态。k8s会通过调度机制来尽量使两个字段相等。  

### 创建对象
用户声明一个对象，就是创建一个对象。这些数据会发送给k8s api,所以要使用json格式。不过kubectl能够接受`yaml`文件  
下面是创建一个对象，必须要包含的几个字段  
- apiVersion
指定使用的API版本
- kind
创建什么种类的对象
- metadata
该类包含一系列的字段，用来作为区分对象的信息如**name**,**UID**,以及**namespace**
- spec
不同k8s对象都是不同的。可以使用该字段中的内嵌内容来指定一些内容  

### 区分不同的对象
k8s中的所有对象利用`name`和`UID`区别。除此之外k8s还提供了不是唯一标识符的`labels`和`annotaions`  
names是用户提供的,并且不能重复的，由`小写字母数字及-.`组成的最长为253字符。  
UID是k8s提供的。每一个对象在创建时就有，直到其被删除  

### 多虚拟集群
一个物理集群支持创建多个虚拟机器。这些虚拟集群被叫做`namespaces`  
其适用于多用户、多team多项目的场景。同一namespace中name对象name不能相等，但不同namespace中name可以相等  
另一方面，还可以通过对不同namespace的资源进行限制  

### 选择和标记
可以为一个对象加上`label`，label是一个key/value对。可以为多个对象但有一定关系的打上label，通过label来直接选中全部。  
通常会将label作为一个索引来用，有些时候对于某些大的或者结构化的数据。没有必要浪费`label`的特性。通常使用`annotaions`  
当前支持两种方式的`label selector`(equality-based和set-based)。用户可以使用它来选择一组对象，一个`label selector`可以有多个需求组成  
其支持`&&`操作  
equality-based操作为`=、==、!=`
set-based操作为`in、notin、exists`

### 注释
k8s支持为对象的`metadata`添加一些注释。其形式也是key/value的格式

```
apiVersion: apps/v1beta1   1.5版本要用`extensions/v1beta1`,1.6版本才有`apps/v1beta1`。1.8版本可以使用`apps/v1beta2`
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
