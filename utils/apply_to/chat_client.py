from socket import *
from time import ctime
import threading

#HOST = '10.10.21.48'
HOST = '10.10.10.110'
PORT = 21568
ADDR = (HOST, PORT)
BUFSIZE = 1024
FLAG = True
from flask import session

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

def send(tcpCliSock):
    try:
        data = '#####%s#####' % session.get('username')
        print(data)
    except Exception as e:
        print(e)
    #tcpCliSock.send(data.encode('utf8'))
    while True:
        data = input('>')
        tcpCliSock.send(data.encode('utf8'))
    tcpCliSock.close()

def recv(tcpCliSock):
    while True:
        data = tcpCliSock.recv(BUFSIZE).decode()
        print(data)
    tcpCliSock.close()

def main():
    t = threading.Thread(name="send", target=send, args=(tcpCliSock,))
    t.start()
    t = threading.Thread(name="recv", target=recv, args=(tcpCliSock,))
    t.start()

if __name__ == "__main__":
    main()
