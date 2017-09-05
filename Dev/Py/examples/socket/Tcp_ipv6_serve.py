import socket
import time
ssss = ('::1',8888)
s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
s.bind(ssss)
s.listen(5)
while True:
    print('Please Waiting for connection')
    cs,address = s.accept()
    print(address)
    # print('the address is %s' % address)
    while True:
        data = cs.recv(1024).decode('utf-8')
        print(data)
        if not data:
            break
        Tm = time.ctime()
        cs.send(("[%s] %s"%(Tm,data)).encode('utf-8'))
