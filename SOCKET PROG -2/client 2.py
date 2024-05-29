from socket import *
from time import sleep
from threading import Thread, Event

RETRY_INTERVAL = 0.01

client = socket()
server_ip = "localhost"
server_port = 56677
print("TRYING TO CONNECT TO THE SERVER\r",end="")
connected = False

while not connected:
    try:
        client.connect((server_ip, server_port))
        print("CONNECTED TO SERVER            ")
        connected = True
    except Exception:
        sleep(RETRY_INTERVAL)

flag = 1
to_person = ""
exit_event = Event()

def receive():
    global flag
    while not exit_event.is_set():
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg:
                if(msg==""):
                    pass
                if msg == "CONNECTED":
                    flag = 0
                elif msg.lower()== "disconnected":
                    print("Connection ended.")
                    print("Press any key to exit")
                    exit_event.set()
                    client.close()
                    break
                else:
                    print(f"[{to_person}]: {msg}")
        except Exception:
            exit_event.set()
            sleep(1)
            print("DISCONNECTED")
            client.close()
            exit()

if connected:
    try:
        msg_from_server = client.recv(1024).decode("utf-8")
        name = input(msg_from_server)
        client.send(name.encode("utf-8"))

        msg_from_server = client.recv(1024).decode("utf-8")
        to_person = input(msg_from_server)
        client.send(to_person.encode("utf-8"))

        receive_thread = Thread(target=receive)
        receive_thread.start()

        while flag == 1 and not exit_event.is_set():
            for i in range(5):
                if exit_event.is_set():
                    break
                print( "*" * i+"\r", end="")
                sleep(0.2)
                print("      \r",end="")
            
       

        if not exit_event.is_set():
            print(f"Connected to {to_person} !!!")
            print("YOU CAN START CHATTING !")

            while not exit_event.is_set():
                try:
                    msg = input()
                    if msg.lower() == "end":
                        client.send("DISCONNECTED".encode("utf-8"))
                        exit_event.set()
                        client.close()
                        exit()
                    else:
                        client.send(msg.encode("utf-8"))
                except Exception:
                    break
        else:
            exit()
    except Exception:
        print("SERVER DISCONNECTED!!!")
        exit_event.set()
        client.close()
else:
    print("Failed to connect to the server after several attempts.")
