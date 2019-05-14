import time
import datetime
from socket import *
from time import ctime
import threading

#HOST = '10.10.21.48'
HOST = '10.10.10.110'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
client = {}

def get_info(tcpCliSock, addr):
    while True:
        data = tcpCliSock.recv(1024).decode()
        if not data:
            break
        if '#####' in data:
            user_name = data.split("######")[1]
            client[addr[0]+':'+str(addr[1])].append(user_name)
        print('[%s][%s] %s' % (addr, ctime(), data))
        
        for i in client.keys():
            info = '[%s] %s' % (ctime(), data)
            client[i][0].send(info.encode('utf8'))
    tcpCliSock.close()

def main():
    while True:
        print('*'*30)
        print(client)
        print("waiting for connection...")
        tcpCliSock, addr = tcpSerSock.accept()
        client[addr[0]+':'+str(addr[1])] = []
        client[addr[0]+':'+str(addr[1])].append(tcpCliSock)
        print("...connected from:", addr)
    
        t = threading.Thread(name="service", target=get_info, args=(tcpCliSock, addr ,))
        t.start()
    tcpSerSock.close()

if __name__ == '__main__':
    main()
