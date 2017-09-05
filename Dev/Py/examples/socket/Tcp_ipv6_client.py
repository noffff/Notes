import socket
Add = ('::1',8888)
Cli = socket.socket(socket.AF_INET6)
Cli.connect(Add)
while True:
    data = 'The client send'
    if not data:
        break
    Cli.send(data.encode('utf-8'))
    data1 = Cli.recv(1024)
    if not data1:
        break
    print(data1.decode('utf-8'))
