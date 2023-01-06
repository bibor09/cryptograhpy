import socket
import threading

class key_server:

    def __init__(self, hostname, port):
        self.clients = dict()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((hostname, port))
        self.socket.listen()
        print('Key server is listening...')

    def recieve(self):
        while True:
            client, client_address = self.socket.accept()
            print(f"Client connected with {str(client_address)}.")

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        while True:
            command = client.recv(1024).decode().split(':')

            # Get key
            if len(command) == 1:
                client_id = command[0]
                if client_id not in self.clients.keys():
                    print("Nonexistent client id.")
                    client.send("0".encode())
                else:
                    print(f'Getting public key for client "{client_id}".')
                    client.send(self.clients[client_id].encode())
            # Register
            elif len(command) == 2:
                print(f'Registering client with id "{command[0]}" and public key "{command[1]}".')
                self.clients[command[0]] = command[1]

key_server = key_server('localhost', 3000)    
key_server.recieve()