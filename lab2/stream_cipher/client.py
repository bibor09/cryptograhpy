import sys
import socket
import threading
from setup import *
from cript import *

def connect(s, algorithm, key):
    while True:
        message = s.recv(4096)
        message = decrypt(message, algorithm, key)
        print(message)

def receive(s, algorithm, key):
    while True:
        message = input()
        
        if message == 'exit':
            sys.exit(0)

        message = encrypt(message, algorithm, key)
        s.sendall(message)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [ip adress] [port]")
        sys.exit(0)

    # create_file()
    algorithm, key = read_from_file()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))

    thread1 = threading.Thread(target = connect, args = ([s, algorithm, key]))
    thread2 = threading.Thread(target = receive, args = ([s, algorithm, key]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()