from random import randint
from time import sleep
from queue import Queue
from MT import My_Thread

def writeQ(queue):
    print("producing object for Q.....")
    queue.put("xxx",1)
    print("size now", queue.qsize())


def readQ(queue):
    val = queue.get(1)
    print("consumed object from Q...size now" , queue.qsize())

def write(queue , loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))

def reader(queue , loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [write , reader]
nfuncs = range(len(funcs))


if __name__ == '__main__':
    nloops = randint(2,5)
    q = Queue(32)

    threads = []
    for i in nfuncs:
        t = My_Thread(funcs[i],(q,nloops),funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print("all Done")


