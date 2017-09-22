from threading import Thread
from time import ctime


class My_Thread(Thread):
    """docstring for My_Thread"""

    def __init__(self, func, args, name=''):
        super(My_Thread, self).__init__()
        self.args = args
        self.name = name
        self.func = func
        # exit(0)

    def run(self):
        print("Starting %s at %s" % (self.name, ctime()))
        self.res = self.func(*self.args)
        print("Ending %s at %s " % (self.name, ctime()))

    def GetResult(self):
        return self.res





def aa(args):
    print(args)
My_Thread(aa, ('a','b'))

