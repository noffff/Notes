# 整形
short int
int
long int
> short 不能比int占用位数多，long不能比int占用位置少。而int的占位是和处理器有关

long long int 至少64位
unsigend int 取值范围  0-65535   16位
在特殊情况需要将小位数的变量强制分配大的空间，<br>如int 7要指为long 7 可以 7L。可以用该方法以此类推7LL
%u    unsigned
%o    八进制
%x    十六进制
%h    short
%ld   long

# 字符串
对于字符的声明定义，其实原理上还是int类型，只不过通过ASCII进行了转换
char test;
test = 'T' 赋值字符,此处不能用"T"，加了""的表示字符串
如果知道一个字符的ASCII也可以使用,ASCII位数来定义
`char test = 65`
> 上面的定义方式在某些时刻可以定义那些**非打印字符**
如定义蜂鸣字符 char test = 7 输出test则会蜂鸣一下，当然对这些字符也可以采用转义方式
回车 \r,换页 \f<F4>
