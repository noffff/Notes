每一个index都会被分成多个shard，每个shard都有自己的副本
ELA副本模型是基于"primary-backup"模型。
primary和replication 都在一个shard replication group中
primary shard是一个shard replication group的入口，对其操作，会影响整个replication group

# basic writing model
每个index操作，首先都会使用route解析为replication group。route默认会使用document id。
当解析成功后，会自动转接到primary shard上。primary将这个操作生效，并且将其应用到副本中，有一个副本清单(in-sync)，primary只用收到这个清单中副本回复的操作成功信息即可
所有操作都会在primary上先执行，然后无误后在传输给副本，副本执行成功后，确认返回。primary将对操作请求返回ack


失败处理
当执行操作因为某些因素失败时，比如 磁盘错误，节点挂了等等。当primary挂了，master会将其他replication节点作为primary。replication 的一个节点挂掉，primary发信息给master将其从 in sync队列移除
