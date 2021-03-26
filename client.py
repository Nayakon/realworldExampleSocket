import threading
import socket

nickname = input("Choose a nickname:")

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM
c.connect(('127.0.0.1', 55555))


def receiving():
    while True:
        try:
            message = c.recv(1024).decode('ascii')
            if message == 'NICK':
                c.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            c.close()
            break


def write():
    while True:
        message = f'{nickname}:{input(" ")}'
        c.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receiving)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
