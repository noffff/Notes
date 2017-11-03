当几个表可能都有一些字段时，可以声明一个类，为该类加入meta类，并为其定义 `abstract=True`属性  
其它类，通过继承这个类中的，来继承该类的所有字段都，该类不会被创建表
```
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```
## 自定义model字段
model提供多种Field，但是也会有没有涉及到的。  
对于这种类型数据支持两种方式  
- 自定义数据字段
- 可以通过python的对象处理，将其转化为符合标准的数据
model字段提供了使用常见python对象的方法，如`string`,`boolean`等  
会将其从一种格式转化为数据库能够处理的格式  
所以要么定义一个Django字段来匹配数据库的字段类型，要么提供一个方法来处理自己的数据  

