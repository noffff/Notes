# kubeadm 安装
运行kubeadm init 可以初始化一个k8s的master节点。初始化的过程有以下几步  
- kubeadm 初始会做一系列的检查。`--skip-preflight-checks`跳过该检查
- kubeadm生成一个token，随后其他节点可以使用该token来向master注册，加入该集群。
- kubeadm 生成一个自签的CA来，来为集群中的其他组件如node签发证书，可以使用`--cert-dir`指定已有的CA路径(默认会使用`/etc/kubernetes/pki`)  
- kubeadm 会在`/etc/kubernets`目录下生成kubelet,controller-manager,scheduler的配置文件。使用其连接API server。
- kubeadm 为API server, controller manager和scheduler server生成静态的Pod
- kubeadm 为将master节点打上标签，这样只让其上面运行控制的组件
- kubeadm 生成允许节点加入时的一些必要的配置文件(安全向) 如  boostrap token和TLS bootstrap的机制
- kubeadm 安装add-on组件(DNS组件)  
  
运行kubeadm join将一个节点加入到集群，会执行以下步骤
- 从API server中下载必须的信息。默认会需要bootstrap toekn和CA key的hash值来确认数据的正确性。
- 一旦确认了集群的信息，kubelet会开始TLS的bootstrap 进程。TLS bootstrap会用share token向Master提交一个CSR,然后Master签名
- 最后,kubeadm会配置本地的kubelet  

