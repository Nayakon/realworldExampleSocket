import threading
import socket

host = '127.0.0.1'  # localhost
port = 55555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

clients = []
nicknames = []


def broadcast(message):  # this for loop si to sent message.
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chart'.encode('ascii'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = s.accept()
        print(f"connection established {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is{nickname}!')  #
        broadcast(f'{nickname} joined the chart!'.encode('ascii'))
        client.send('Connect to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is waiting")
recieve()
