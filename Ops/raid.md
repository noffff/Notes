# 优化前的知识
- 当前RAID的类型
- raid阵列中的要有大于1块的磁盘
- RAID磁盘的CHUNK大小
- 文件系统的block-size

## RAID chunk size
不可能永远即对多个磁盘进行平行的写入。假设两个硬盘写入一字节，那么每个磁盘上要写4位，理论上讲，这样的操作应该是这个磁盘写1位那个磁盘写1位。  
但是，实际上硬件是不支持这种操作。一般为设备设定一个可写入的最小`chunk size`，该chunk size是原子操作的最小块大小。  
例如，一个对chunk size为4k的16k写入操作，其第一个和第三个chunk size会写入到第一块磁盘，第二和第四个chunk size写到第二块磁盘  
格式化时加入stride和strip width是为了让卷能够与RAID的条带大小对齐，从而提高性能。这样可以避免在文件系统中重复的计算和调整，使系统数据更容易的写入到磁盘中  

stride size = chunk size/block size
strip width = stride size * number of data_disk
