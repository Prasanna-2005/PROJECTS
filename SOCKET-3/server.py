import curses
from time import sleep
import socket
from threading import Thread,Event,Lock

e = Event()
t_lock = Lock()
greenlist = [] #even id players
redlist = [] # PLAYERS WHO ARE WAITING FOR OPPONENTS with odd id
names = {}  # Maps username to socket
try:
    server = socket.socket()
    server_ip = "localhost"
    port = 56677
    server.bind((server_ip, port))
    server.listen(10)
    print("WAITING FOR CLIENTS")
except Exception:
    print("CHECK IP/PORT NOT AVAILABLE")
    exit()

def cleanup(name,id):

    t_lock.acquire()

    if id in names:
        del names[id]
        print("Socket History updated -",id)
    if id in redlist :
        redlist.remove(id)
    elif id in greenlist:
        greenlist.remove(id)

    t_lock.release()

    print("Active list updated - ", name)
    client_socket.close()
    print(f"[{name} {id}]:::removed")


def connect_oppo(): #global thread
    while(1):
      try: 
        if(greenlist and redlist):
            oppo1 = greenlist.pop(0)
            oppo2 = redlist.pop(0)

            code2 = str(oppo2) + 'R'
            code1 = str(oppo1) + 'G'

            oppo1soc = names[oppo1]
            oppo2soc = names[oppo2]

            oppo1soc.send(code2.encode())
            oppo2soc.send(code1.encode())
            print(oppo1,"picked")
            print(oppo2,"picked")
      except Exception as e:
          print(e)
          continue
         
def game_server(player_socket,oppo_socket,name,id):
    try:
     while(1):
        player_move = player_socket.recv(1024).decode()   #1st letter == L/R/T/B remaining tells cell id
        oppo_socket.send(player_move.encode())

    except:
      oppo_socket.send("121".encode())
      print("NOTIFICATION SENT")
      cleanup(name,id)

def connection(client_socket,id,uname,color):
    print(f"{uname} Connected")
    try:
        names[id] = client_socket
        if(color == "G"):
            greenlist.append(id) 
        else:
            redlist.append(id)
        oppo_id = int(client_socket.recv(1024).decode())
        opposoc = names[oppo_id]
        game_server(client_socket,opposoc,uname,id) 
        
    except:
        cleanup(uname,id)

id =0
oppoconnect = Thread(target=connect_oppo)
oppoconnect.start()
while True:
    try:
        client_socket, client_address = server.accept()
        uname = client_socket.recv(1024).decode()
        id = id+1
        color = "R" if id%2==1 else "G"
        thread = Thread(target=connection,name=str(id),args=(client_socket,id,uname,color))
        thread.start()
    except Exception:
        pass

