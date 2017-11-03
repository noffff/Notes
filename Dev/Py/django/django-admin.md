Django自带的项目管理工具  
## 自动创建项目
django-admin.py startproject 项目名
会自动生成几个文件  
- manage.py  
应用命令行接口
- settings.py  
项目相关的配置
- urls.py  
全局URL配置
### 创建项目下的应用
manage.py startapp app_name  
生成以下文件  
- urls.py
应用的URL配置文件
- views.oy
视图函数
- tests.py
单元测试  
生成app后需要在Django的`settings.py`文件中的`INSTALLED_APPS`中加入该`app_name`  
再为Django添加一个app后需要执行`manage.py migrate`操作用来在数据库中创建对应的表  
### Django 处理流程
自底向上  
- 首先查找匹配的URL模式，
- 调用对应的视图函数
- 最后将渲染好的数据通过模板展现
