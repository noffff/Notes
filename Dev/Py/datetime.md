# datetime Module
该模块主要用来处理时间方面的问题。提供多种复杂、简单的解决方案
----
- Subclss
  - timedelta
  - tzinfo
  - time
  - date
  - datetime
模块的日期时间数据分为两种
- naive
naive对象类型的数据，如同字面意思，简单，没有复杂的格式,因此也不能非常准确的表明时间日期数据。<br>其值只取决于数字，不考虑失去问题
> 上述准确只是相对于aware格式
- aware
包含较多的信息，如时区、夏令时等
> 两类最明显区别就是是否包含时区
----
datatime和time两个对象都的tzinfo是可选的。<br>tzinfo可以设置为一个实例，这个对象主要用来存放针对UTC时区时间的偏移量，时区的名字，已经是否有夏令时的影响,然而比较坑爹的是这样一个时间处理库，自身竟然没有带详细的tzinfo，
一般使用时区的偏移量等可以使用pytz及 dateutil.tz.gettz(tz)
# datetime
这个类能够将time类和date类的数据进行拼装组合，处理。
一般做时区转换时，因为其能够同时处理时间和日期，所以使用该方法。

# time
如其字面意思 用来处理分钟、小时、秒、毫秒、和时区

# date
处理年、月、日

# timedelta
用来处理两个时间数据之间的关系，比如指定一个日期时间，然后在这个日期时间上进行一定时间的推移，计算出推移后的日期时间

# tzinfo
时区对象。可以用户自定义

# 转换时区的思路
将时间转换成datetime能够处理的格式，然后指定其时区信息
[时间格式表](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)
