import sys
import socket
import threading
import merkell_knapsack
import solitaire
import cript
from ast import literal_eval

KEY_SERVER_HOSTNAME = 'localhost'
KEY_SERVER_PORT = 3000

def recieve_from_client(socket, seed):
    while True:
        message = socket.recv(1024)
        message = cript.decrypt(message, solitaire.generate_key_with_solitaire, seed)
        print(message)

def send_to_client(socket, seed):
    while True:
        message = input()
        message = cript.encrypt(message, solitaire.generate_key_with_solitaire, seed)
        socket.send(message)

def log_seed(seed):
    print('-----------------------------------------------------\n')
    print("The solitaire seed: \n", seed)
    print('-----------------------------------------------------\n')

def convert_str_to_ints(str):
    return literal_eval(str)

def convert_ints_to_str(array):
    return '[' + ','.join([str(i) for i in array]) + ']'
    

class client:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.private_key = merkell_knapsack.generate_private_key(8)
        self.public_key = merkell_knapsack.create_public_key(self.private_key)
        self.seed = []

        # Connecting to key server
        self.sock_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_to_server.connect((KEY_SERVER_HOSTNAME, KEY_SERVER_PORT))
        print(f"Client connected to key server on {KEY_SERVER_HOSTNAME}:{KEY_SERVER_PORT}")

        # Listening on assigned hostname and port
        self.socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket1.bind((hostname, port))
        self.socket1.listen()
        print(f"Client assigned to {self.hostname}:{self.port}\n")

        # Initializing threads
        self.receiving_thread = threading.Thread(target = self.recieve_client, args = ([])) 

    # SERVER COMMUNICATION   
    def register_on_connection(self):
        self.sock_to_server.send(f"{self.port}:{self.public_key}".encode())
        print("Registered succesfully.")

    def register(self):
        self.sock_to_server.send(input("Please enter [client id]:[public key]!\n").encode())

    def get_key(self):
        print("Please enter client id!")
        client_id = input()
        self.sock_to_server.send(client_id.encode())

        public_key = self.sock_to_server.recv(1024).decode()
        if public_key == "0":
            print("Nonexistent client id.")
        else:
            print(f"Got public key '{public_key}' for client with id '{client_id}'.")
            return convert_str_to_ints(public_key)

    # RECEIVING FROM CLIENT COMMUNICATION
    def recieve_client(self):
        client, client_address = self.socket1.accept()
        print(f"Client connected with {str(client_address)} and wants to chat.")

        self.console_stop = True

        # If received connection: has to decode solitaire seed, and after that they can communicate
        cipher_text = convert_str_to_ints(client.recv(1024).decode())
        self.seed = merkell_knapsack.decrypt_mh(cipher_text, self.private_key)                                  # KNAPSACK for decryption
        log_seed(self.seed)

        # After key exchange they can communicate
        print("Chat started\n")
        thread1 = threading.Thread(target=recieve_from_client, args=(client, self.seed))
        thread2 = threading.Thread(target=send_to_client, args=(client, self.seed))
        thread1.start()
        thread2.start()

    # MAIN THREAD    
    def go(self):
        self.register_on_connection()
        self.receiving_thread.start()
        self.receiving_thread.join()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [client hostname] [client port]")
        sys.exit(0)

    client = client(sys.argv[1], int(sys.argv[2]))
    client.go()
