# 使用方法
- 输入输出
  - -r 从文件中读已有的包信息
  - -w 将输出写入到文件中
  - -V 从文件中读取一系列的包文件
  - -S 每一次输出完整序号数太大，太麻烦。所以只输出相对初始序号的偏移量。加上该参数关闭该功能。
# 输出解释
- TCP三次握手
```
15:02:35.255401 IP vm1.55460 > vm2.zabbix-agent: Flags [S], seq 4242511755, win 29200, options [mss 1460,sackOK,TS val 130354056 ecr 0,nop,wscale 7], length 0
15:02:35.255654 IP vm2.zabbix-agent > vm1.55460: Flags [S.], seq 1827300432, ack 4242511756, win 28960, options [mss 1460,sackOK,TS val 20272539 ecr 130354056,nop,wscale 7], length 0
15:02:35.255682 IP vm1.55460 > vm2.zabbix-agent: Flags [.], ack 1827300433, win 229, options [nop,nop,TS val 130354057 ecr 20272539], length 0
```
- TCP四次分手
```
15:02:38.257104 IP vm2.zabbix-agent > vm1.55460: Flags [F.], seq 1827300433, ack 4242511756, win 227, options [nop,nop,TS val 20275540 ecr 130354057], length 0
15:02:38.257276 IP vm1.55460 > vm2.zabbix-agent: Flags [F.], seq 4242511756, ack 1827300434, win 229, options [nop,nop,TS val 130357058 ecr 20275540], length 0
15:02:38.257739 IP vm2.zabbix-agent > vm1.55460: Flags [.], ack 4242511757, win 227, options [nop,nop,TS val 20275541 ecr 130357058], length 0
```
- 标志意思
  - cksum:校验和
  - vm1xxx > vm2xxx:[xxx] <br>表示 源>目的:标志
