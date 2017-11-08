# 用户侧的状态
- NEW
这个包是第一次出现。意味着conntrack模块发现了一个新的包。例如一个包里包含了`SYN`。
- ESTABLISHED
- RELATED
该状态实在ESTABLISHED之后的。由ESTABLISHED连接衍生的连接。
- INVALID
代表不能识别的状态
- UNTRACKED
raw表为包打了untracked标记的包的状态

