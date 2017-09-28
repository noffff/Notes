## 定义一个Service
创建的也是一个REST对象。类似于Pod的。  
下面创建一个都暴露9376端口并且携带一个label标签(app=NyApp)
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
上面这个描述，会创建一个名字为`my-service`的Service对象。这个Service会被分配一个IP地址有时也叫cluster IP。Service的`selector`会连续进行筛选工作并且结果传入一个也叫做**my-service**的`Endpoints`对象  

