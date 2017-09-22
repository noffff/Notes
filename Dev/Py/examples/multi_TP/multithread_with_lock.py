from atexit import register
from random import randrange
from threading import Thread, currentThread, Lock
from time import sleep, ctime


class CleanOutputSet(set):

    def __str__(self):
        return ','.join(x for x in self)

loops = (randrange(2, 5) for x in range(randrange(3, 7)))
remaining = CleanOutputSet()
lock = Lock()

def loop(nsec):
    myname = currentThread().name
    remaining.add(myname)
    lock.acquire()
    print('%s Started %s' % (ctime(), myname))
    sleep(nsec)
    remaining.remove(myname)
    print("%s Complete %s %s" % (ctime(), myname, nsec))
    print("remaining %s" % (remaining or 'None'))
    lock.release()


def main():
    for pause in loops:
        Thread(target=loop, args=(pause,)).start()


@register
def exit():
    print("all Done at:", ctime())


main()

