from socket import *
from time import ctime
import threading

HOST = '10.10.21.48'
PORT = 21567
ADDR = (HOST, PORT)
BUFSIZE = 1024

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

def send(tcpCliSock):
    while True:
        data = raw_input('>')
        tcpCliSock.send(data)
    tcpCliSock.close()

def recv(tcpCliSock):
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        print data
    tcpCliSock.close()

def main():
    t = threading.Thread(name="send", target=send, args=(tcpCliSock,))
    t.start()
    t = threading.Thread(name="recv", target=recv, args=(tcpCliSock,))
    t.start()

if __name__ == "__main__":
    main()
