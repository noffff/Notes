# 概念
为了使方法或函数的改变变的方便  
装饰器的基础是函数是对象，对象可以赋值给其他变量，可以传递操作  
**装饰器就是一层一层封装的过程，每一层返回其包含的下一层的函数对象**
在过去的方法中，通常多种变量的传递来完成这项工作如  
```
def decorator_maker():                                                                                
                                                                                                      
    print("I make decorators! I am executed only once: "                                              
          "when you make me create a decorator.")                                                     
                                                                                                      
    def my_decorator(func):                                                                           
                                                                                                      
        print("I am a decorator! I am executed only when you decorate a function.")                   
                                                                                                      
        def wrapped():                                                                                
            print("I am the wrapper around the decorated function. "                                  
                  "I am called when you call the decorated function. "                                
                  "As the wrapper, I return the RESULT of the decorated function.")                   
            return func()                                                                             
                                                                                                      
        print("As the decorator, I return the wrapped function.")                                     
                                                                                                      
        return wrapped                                                                                
                                                                                                      
    print("As a decorator maker, I return a decorator")                                               
    return my_decorator                                                                               
                                                                                                      
                                                                                                      
def decorated_function():                                                                             
    print("I am the decorated function.")                                                             
# ------------------                                                                                                  
new_decorator = decorator_maker()                                                                     
decorated_function = new_decorator(decorated_function)                                                
decorated_function()                                                                                  
                                                                                               
```  
其中从`# -------`开始就是通过中间变量，最后使用`decorated_function()`获取decorator_maker最里层的东西。  
上面这种写法非常不美观，所以可以换用一种方法,只从`# ------`下开始  
```
decorated_function = decorator_maker()(decorated_function) 
decorated_function()   
``  
至此可将其换位`@`标记的装饰器
```
@decorator_maker()                                                 
def decorated_function():                                          
    print("I am the decorated function.")                          
decorated_function()                                               
```
## 语法
装饰器参数只能是一个，不论形式，只能是一个，因为这个特性传入多值可用*args或**kwargs  
```
@dec2
@dec1
def func():
    pass
```
等价于
```
def func():
    pass
func = dec2(dec1(func))
由上至下对应由外到内,有下至上进行封装
```
### 给被装饰的函数传参数  
```
def Foo(func):
    def wrapper(*args):
        func(args)
        print('aaaaa')
    return wrapper

@Foo
def Foo1(*args):
    print('bbbbb')
    print(args)
```
### 给装饰器传参  
默认装饰器只能接受一个参数，而这个位置一般被`被修饰的函数对象`所占用  
因此不能直接给装饰器传参,所以我们可以再在外面套一层，用来接收其他相关参数。如
```
def pre_Foo(*args):
    def Foo(func):
        def wrapper(*args):
            func(args)
            print('aaaaa')
        return wrapper
    return Foo

@pre_Foo('a')
def Foo1(*args):
    print('bbbbb')
    print(args)
```
[参考]{https://stackoverflow.com/a/1594484/7566324}


# 元类
类是描述如何生成一个对象的代码段，但是类本身也是一个对象。因此利用python中对象的性质，可以  对该对象进行操作如、增加一个属性、方法、赋值给一个变量、将其作为参数传递  
当调用class时，就是通过元类来动态实现的  
**元类就是用来创建`类`的东西**。元类就是类的类。`type`函数就是一个元类。其不单单是显示对象类型  
还能够通过接收一个类的描述作为参数，从而返回一个类
```
b = type('b',(),{'abc':123})
```
一般创建类的时候可以为类加上`__metaclass__`属性，如下  
```
class FFF(object):
    __metaclass__ = xxx
```
在解释器发现声明class FFF时解释器会去找元类，如果没找到就会用type去创建。  
```
class Foo(Bar):
pass
```
**python处理上述代码时做了下面这些事情**  
1.在Foo中是否有__metaclass__，如果有就在内存中通过元类创建一个Foo类的对象，不是类是对象。  
如果没有找到就会在模块层中去找。  
如果还没有找到就会去使用`Bar`的(Bar中可能就是默认的`type`元类)  
`__metaclass__`属性是不被继承的。如果`Bar`使用一个`__metaclass__`通过type()元类的属性创建了`Bar`(不是type.__new__()，__new__是创建一个完整的类，不是调用)。子类不会继承。  
`__metaclass__`用来放置能够创建类的东西，比如说`type`或其他子类使用的东西

## 自定义元类
待续
[摘自](https://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python)


