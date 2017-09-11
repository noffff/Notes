import threading
from time import ctime, sleep


class Do(threading.Thread):

    def __init__(self, func, *args, name = 'ABC'):
        super(Do, self).__init__()
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        print('Start %s at %s' % (self.name, ctime()))
        self.func(self.args[0][1])
        print('Done %s at %s' % (self.name, ctime()))


def loop(seconds):
    sleep(seconds)

if __name__ == '__main__':
    threads = []
    loops = [4, 2]
    for i in range(2):
        T = Do(loop, (i, loops[i]) , name = str(loops[i]))
        threads.append(T)

    for i in range(2):
        threads[i].start()

    for i in range(2):
        threads[i].join()
    print('finish at ', ctime())

