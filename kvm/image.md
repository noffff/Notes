该image不是`镜像`的意思。在虚拟化中虚拟磁盘统称为`image`  
创建iamge `qemu-img create -f raw centos7.4_base.raw 20G`  
## 磁盘种类
### raw
用多少占多少。可转化为其他格式  
可以作为后端镜像  
### qcow2
用多少占多少。只能转化为raw格式  
支持加密、压缩、快照等功能  
可以作为后端镜像,可以在后端镜像基础上建立差量镜像  
如
