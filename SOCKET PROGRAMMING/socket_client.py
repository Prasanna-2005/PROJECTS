import threading
import time
from socket import *

def blink_dots(stop_event):
    while not stop_event.is_set():
        for i in range(8):
            if stop_event.is_set():
                print("\r            ", flush=True)
                break
            dots = '.' * i
            print(f'\rConnecting{dots}', end='', flush=True)
            time.sleep(0.1)
        if(not stop_event.is_set()):
          print("\rConnecting       ", end='', flush=True)

def run_client():
    client = socket()
    stop_event = threading.Event()
    server_ip = "localhost"
    server_port = 56677
    retry_interval = 1
    print("TRYING TO CONNECT TO THE SERVER")
    connected = False
    
    blink = threading.Thread(target=blink_dots, args=(stop_event,))
    blink.daemon = True
    blink.start()

    while(not connected):
        try:
            client.connect((server_ip, server_port))
            connected = True
            stop_event.set()  # Signal the blinking thread to stop
            break
        except Exception:
            time.sleep(retry_interval)

    if connected:
        try:
            print("\rConnected to the server!           ")  
            print("You can now start chatting!!")
            print("-" * 50, "\nYou can end chat by typing 'close'\n" + "-" * 50)
            while True:
                msg_to_server = input()
                client.send(msg_to_server.encode("utf-8"))
            
                msg_from_server = client.recv(1024).decode("utf-8")
                print(f"[S] {msg_from_server}")
                if msg_from_server.lower() == "closed":
                    print("Server closed the connection")
                    break
        except Exception :
            print(f"SERVER DISCONNECTED!!!")
        finally:
            client.close()
    else:
        print("Failed to connect to the server after several attempts.")

run_client()
