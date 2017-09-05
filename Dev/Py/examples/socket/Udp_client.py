import socket
ADD = ('::1',9999)
udp_Client = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
while True:
    data = 'this is udp message'
    if not data:
        break
    udp_Client.sendto(data.encode('utf-8'),ADD)
    data,ADD = udp_Client.recvfrom(1024)
    if not data:
        break
    print(data.decode('utf-8'))
