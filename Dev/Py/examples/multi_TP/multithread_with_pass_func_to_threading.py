import threading
from time import ctime, sleep

loops = [4, 2]


def loop(loop_number, second):
    print('Start loop: %s start at: %s' % (loop_number, ctime()))
    sleep(second)
    print('Start loop: %s End at: %s' % (loop_number, ctime()))


def main():
    print('This func start at ', ctime())
    threads = []
    nloops = range(2)
    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('All done at:', ctime())

main()
