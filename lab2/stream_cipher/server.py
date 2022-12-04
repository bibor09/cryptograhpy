import socket
import threading
import sys
from setup import *
from cript import *

def recieve(connection, algorithm, key):
    while True:
        message = connection.recv(4096)
        message = decrypt(message, algorithm, key)
        print(message)

        if message == 'exit':
            break

def send(connection, algorithm, key):
    while True:
        message = input()

        if message == ' ':
            pass
        if message == 'exit':
            sys.exit(0)
        else:
            message = encrypt(message, algorithm, key)
            try:
                connection.sendall(message)
            except:
                sys.exit(0)

if __name__ == '__main__':
    # generate file
    algorithm, key = read_from_file()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 1500))
    s.listen()
    (connection, address) = s.accept() 

    thread1 = threading.Thread(target = recieve, args = [connection, algorithm, key])
    thread2 = threading.Thread(target = send, args = [connection, algorithm, key])
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()