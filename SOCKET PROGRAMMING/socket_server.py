MAX_CLIENT_QUEUE = 2
from socket import *

def run_server():
    try:
        server = socket()
        server_ip = "localhost"
        port = 56677
        server.bind((server_ip, port))
        server.listen(MAX_CLIENT_QUEUE)
        
        
        while True:
            try:
                print("WAITING FOR CLIENT TO CONNECT")
                client_socket, client_address = server.accept()
                client_ip = client_address[0]
                client_port = client_address[1]
                print(f"CONNECTED TO THE CLIENT {client_ip}:{client_port}!")
                print("YOU CAN NOW START CHATTING")

                while True:
                    msg_from_client = client_socket.recv(1024).decode("utf-8")
                    
                    print(f"[C] {msg_from_client}")
                    if msg_from_client.lower() == "close":
                        print("Connection closed by client...")
                        client_socket.send("Closed".encode("utf-8"))
                        break
                    else:
                        msg_to_client = input()
                        client_socket.send(msg_to_client.encode("utf-8"))
                client_socket.close()
            except Exception:
                print(f"Client Disconnected")
            finally:
                client_socket.close()
    except Exception :
        print(f"UNABLE TO CREATE SERVER!! TRY AGAIN: ")
    finally:
        server.close()

run_server()
