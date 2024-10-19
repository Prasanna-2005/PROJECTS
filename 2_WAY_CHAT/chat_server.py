from socket import *
from time import sleep
from threading import Thread

MAX_CLIENT_QUEUE = 3

pairs = []  # (n, p) stores (from, to)  
names = {}  # socket history 


try:
    server = socket()
    server_ip = "localhost"
    port = 56677
    server.bind((server_ip, port))
    server.listen(MAX_CLIENT_QUEUE)
    print("WAITING FOR CLIENTS")
except Exception :
    print("CHECK IP/PORT NOT AVAILABLE", )


def send_to(target_socket, encoded_msg):
    try:
        target_socket.send(encoded_msg.encode("utf-8"))
    except Exception:
        pass


def handle(client_socket, name, pname):
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                send_to(names[pname], message)
            except :
                  pairs.remove((name, pname))
                  print("Client's pair removed")  
                  if name in names:
                      del names[name]
                  client_socket.close()
                  break
def info(client_socket):
    name = ""
    pname = ""
    try:
        client_socket.send("What is your name? ".encode("utf-8"))
        name = client_socket.recv(1024).decode("utf-8")

        client_socket.send("Whom do you want to talk to? ".encode("utf-8"))
        pname = client_socket.recv(1024).decode("utf-8")

        names[name] = client_socket
        pairs.append((name, pname))

        while True:
            try:
                if (pname, name) in pairs:
                    break
                client_socket.send("".encode("utf-8"))
            except :
                pairs.remove((name, pname))
                del names[name]
                print("Disconnected Client's pair removed") 
                client_socket.close()

        client_socket.send("CONNECTED".encode("utf-8"))
        connection_thread = Thread(target=handle, args=(client_socket, name, pname))
        connection_thread.start()

    except (ConnectionAbortedError, ConnectionError, Exception):
        if (name, pname) in pairs:
            pairs.remove((name, pname))
            print("Disconnected Client's pair removed")    
        if name in names:
            del names[name]
        client_socket.close()


while True:
    try:
        client_socket, client_address = server.accept()
        info_thread = Thread(target=info, args=(client_socket,))
        info_thread.start() 
    except OSError or Exception: 
        pass
