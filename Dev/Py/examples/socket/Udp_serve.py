import socket
import time
ADD = ('::1',9999)
udp_Socket = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
udp_Socket.bind(ADD)
while True:
    print('waitting for message')
    data,add = udp_Socket.recvfrom(1024)
    udp_Socket.sendto(('[%s] %s'%(time.ctime(),data)).encode('utf-8'),add)
    print('recvived from and returned to :',add)
