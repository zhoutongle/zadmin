import time
import datetime
from socket import *
from time import ctime
import threading

HOST = '10.10.21.48'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
client = {}

def get_info(tcpCliSock, addr):
    while True:
        data = tcpCliSock.recv(1024)
        if not data:
            break
        print('[%s][%s] %s' % (addr, ctime(), data))
        for i in client.keys():
            client[i].send('[%s] %s' % (ctime(), data))
    tcpCliSock.close()

def main():
    while True:
        print('*'*30)
        print(client)
        print("waiting for connection...")
        tcpCliSock, addr = tcpSerSock.accept()
        client[addr[0]+':'+addr[1]] = tcpCliSock
        print("...connected from:", addr)
    
        t = threading.Thread(name="service", target=get_info, args=(tcpCliSock, addr ,))
        t.start()
    tcpSerSock.close()

if __name__ == '__main__':
    main()
