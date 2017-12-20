## 定义一个Service
创建的也是一个REST对象。类似于Pod的。  
下面使用模板创建一个Service
```
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
```   
上面的模板描述，会创建一个名字为`my-service`，暴露9376端口,并且携带一个label标签(app=MyApp)service对象。  
service可以根据不同的`type`分配不同种类的地址  
- ClusterIP(默认)
分配一个k8s集群中ip，通俗来说就是将服务只暴露在集群中  
- NodePort
通过NAT方式，将服务端口暴露在选中的Node上。  
- LoadBalancer
如果当前平台支持LB功能，那么会创建一个额外的LB。  
- ExternalName
为服务指定一个随意的名字，作为`CNAME`记录。该类型需要大于等于1.7版本的kube-dns
