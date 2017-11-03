在初始项目的根下创建`.gitlab-ci.yml`，如果已经配置好了Runner，那么ci会自动去读取该文件  
可以在该文件中定义多个job，每个job的名称作为最顶级的存在，并且名字自拟(不能使用关键字)，每个job至少要包含一个`script`,每个job的执行都是相互独立的  
`.gitlab-ci.yml`会告诉ci runner做什么，如何去做(按照job的描述)。每个job，默认分为三个`stage`。  
- build
- test
- deploy
在文件中三个阶段不必都声明，如果不声明会忽视该阶段的工作  
如果该文件中有`before_script`那么在执行文件中的所有job的开始时都会执行一次。同理`after_script`亦然  
```
image: ruby:2.1
services:
  - postgres
before_script:
  - bundle install
after_script:
  - rm secrets
stages:
  - build
  - test
  - deploy
job1:
  stage: build
  script:
    - execute-script-for-job1
  only:
    - master
  tags:
    - docker
```
gitlab 检测文件的有效性`CI/CD ➔ Pipelines and Pipelines ➔ Jobs`或`gitlab_url/ci/lint`  
## docker
`image`关键字定义使用什么样的镜像  
可以使用`pull_policy`定义镜像pull的策略，默认为always  
`service`关键字定义另外一个镜像，使job定义的`image`镜像与其建立联系。从`image`定义的镜像连接`service`定义的容器服务时，主机地址== `service`定义的镜像名，如果有`/`换位`__`或`-`。`:*`抛弃。如果使用这样的主机名感觉别扭可以使用如下方法
```
services:
- name: my-postgres:9.4
  alias: db-postgres
```
