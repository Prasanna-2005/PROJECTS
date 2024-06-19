
import socket
import curses
from threading import Thread,Event,Lock
from curses import textpad
from time import sleep
from curses import wrapper

e = Lock()
#GRID 7 * 7   7blocks each side
# 8rows or 8lines
# 8cols or 8chars
CELL_HEIGHT = 3 # 4 lines
CELL_WIDTH = 6 # 7 characters
max_wins = 0
name_reg = 0
allcell = []

GRID = 7
LEFT_PAD = 10 + 13 #13 outsise + 10 inside gamewindow
TOP_PAD = 4

menu = ['CONNECT THE DOTS','','CONNECT TO PLAY', 'EXIT']
#   256colorpairs    756colors


class cells:
        def __init__(self, row, col):
                    self.cid = row * 7 + col
                    self.neighbours = []
                    if self.cid == 0:
                        self.neighbours = [self.cid + 7, self.cid + 1]
                    elif self.cid == (GRID-1):
                        self.neighbours = [self.cid + 7, self.cid - 1]
                    elif self.cid == (GRID*(GRID-1)):
                        self.neighbours = [self.cid - 7, self.cid + 1]
                    elif self.cid == (GRID*GRID)-1:
                        self.neighbours = [self.cid - 7, self.cid - 1]
                    elif self.cid in range(1, GRID-1):
                        self.neighbours = [self.cid + 7, self.cid + 1, self.cid - 1]
                    elif self.cid in range(GRID, GRID*(GRID-1), GRID):
                        self.neighbours = [self.cid + 7, self.cid + 1, self.cid - 7]
                    elif self.cid in range(2*GRID-1, (GRID*GRID)-1, GRID):
                        self.neighbours = [self.cid + 7, self.cid - 1, self.cid - 7]
                    elif self.cid in range((GRID*(GRID-1)), (GRID*GRID)-1):
                        self.neighbours = [self.cid - 7, self.cid + 1, self.cid - 1]
                    else:
                         self.neighbours = [self.cid - 7,self.cid+7, self.cid + 1,self.cid-1]
                    
                    self.c_filled = 0

                    self.left = 23+(col*6)
                    self.right= self.left + 6
                    self.top = 4+(row*3)
                    self.bottom = self.top +3

                    self.sides = [0,0,0,0]  #    top,right,bottom,left

                    self.cellmid_y = (self.top + self.bottom)//2
                    self.cellmid_x = (self.left + self.right)//2

                    self.win =None
                    self.edges= [
                          [(self.left,self.top),(self.right,self.top)],  #top(0,1)
                          [(self.right,self.top),(self.right,self.bottom)],    #right  (2,3) 
                          [(self.left,self.bottom),(self.right,self.bottom)],  #bottom(4,5)
                           [(self.left,self.bottom),(self.left,self.top)],  #left  (6,7)
                          ]   


        def cellfilled(mainwin,color):  #fill cell if got 4 edges
            for i in allcell:
              if 0 not in i.sides and not i.c_filled:
                    x = curses.newwin(2,5,i.top+1,i.left+1)
                    x.bkgd(' ',curses.color_pair(color)| curses.A_REVERSE)
                    i.c_filled = 1
                    i.win = ('R' if color == 1 else 'G')
                    mainwin.refresh()
                    x.refresh()


        def give_obj_for_id(id):
              for i in allcell:
                    if(i.cid==id):
                          return i
                    

        def set_edge_true(self,index,edge):  #updates edges on entire board
              edge1 = edge
              edge2 = [edge[1],edge[0]]
              for i in self.neighbours:
                    cellobj = cells.give_obj_for_id(i)
                    if edge1 in cellobj.edges  :
                          ind = cellobj.edges.index(edge1)
                          if cellobj.sides[ind] == 0:
                              cellobj.sides[ind] = 1
                    elif edge2 in cellobj.edges:
                          ind = cellobj.edges.index(edge2)
                          if cellobj.sides[ind] == 0:
                            cellobj.sides[ind] = 1
    

        def modify(self,window,color,which_side):  #red->1  green->1   draw hline and vline  
             curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
             curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
             for i,side in enumerate(self.sides):
                if(side and i==which_side):
                        y, x = window.getyx()
                        window.attron(curses.color_pair(color))
                        if i == 0:  # top
                            window.hline(self.top, self.left+1, "-", 5)
                            cells.cellfilled(window,color)
                        elif i == 2:  # bottom
                            window.hline(self.bottom, self.left+1, "-", 5)
                            cells.cellfilled(window,color)
                        elif i == 1:  # right
                            window.vline(self.top+1, self.right, '|', 2)
                            cells.cellfilled(window,color)
                        elif i == 3:  # left
                            window.vline(self.top+1, self.left, '|', 2)
                            cells.cellfilled(window,color)
                window.attroff(curses.color_pair(color))
                window.refresh()

def num_box_filled_red():
     r_pts = 0
     for i in allcell:
          if(i.win != None):
               if(i.win=='R'):
                    r_pts+=1
     return (r_pts)   
  
def num_box_filled_green():
     g_pts = 0
     for i in allcell:
          if(i.win != None):
               if(i.win=='G'):
                    g_pts+=1
     return (g_pts)

def display_rules(mainwin,color):
     c = "RED" if color == 'R' else 'GREEN'
     cnum = 1 if c=="RED" else 2
     mainwin.clear()
     msg =[f"YOU ARE {c}"," ","RULES"," "," ","1.RED TAKES TURN FIRST , THEN GREEN FOLLOWS "," ","2.TURN IS DENOTED BY COLOR ON RIGHT WINDOWS"," ","3.TO DRAW LINES ,SELECT CELL USING CURSOR,DONT USE TRACK PADS","PS:TO SELECT ANOTHER CELL,JUST CLICK TO DESELECT,SELECT AGAIN"," ","4.USE ARROWS TO SELECT EDGE OF THE CELL"]
     for i,j in enumerate(msg):
          mainwin.addstr(height//2 - 8 + i, width//2 - (len(j))//2,j,curses.color_pair(cnum))
          mainwin.noutrefresh()
     mainwin.refresh()
     mainwin.addstr(height//2 - 3 + 12, width//2 - (len("CLICK PRESS ENTER TO CONTINUE..."))//2,"PRESS KEY TO CONTINUE...",curses.color_pair(2))
     mainwin.getch()
     mainwin.clear()
     mainwin.refresh() 

def display_winner(mainwin):
    rp = num_box_filled_red()
    gp = num_box_filled_green('G')[1]
    mainwin.clear()
    winner = 1 if rp > gp else 0
    if(rp>gp):
         mainwin.addstr(height//2,width//2 -4,"RED WON")
    elif(gp>rp):
         mainwin.addstr(height//2,width//2 -4,"GREEN WON")
    mainwin.refresh()
    return winner           


def initiate_draw_edge(mainwin,i,edgeindex,color):
            mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
            mainwin.refresh()
            i.sides[edgeindex]=1
            i.set_edge_true(edgeindex,i.edges[edgeindex])
            i.modify(mainwin,color,edgeindex)   


def inspect(x,y,mainwin,color):
                f = ''
                for i in allcell:
                    x_range = (i.left,i.right)
                    y_range = (i.top ,i.bottom)
                    if(x in range(x_range[0],x_range[1]+1)) and (y in range(y_range[0],y_range[1]+1)):
                          mainwin.addstr(i.cellmid_y,i.cellmid_x,".")
                          mainwin.refresh()
                          next_click = mainwin.getch()
                          if next_click == curses.KEY_LEFT:
                                index = 3   #left edge
                                if(not i.sides[3]):
                                    initiate_draw_edge(mainwin,i,index,color)
                                    cellid = str(i.cid).zfill(2)
                                    f="L"+f"{cellid}"+"3"
                                    break
                          elif next_click == curses.KEY_RIGHT: 
                                index = 1   # right edge
                                if(not i.sides[1]):
                                    initiate_draw_edge(mainwin,i,index,color)
                                    cellid = str(i.cid).zfill(2)
                                    f="R"+f"{cellid}"+"1"
                                    break                             
                          elif next_click == curses.KEY_DOWN:
                                index = 2    #bottom edge
                                if not(i.sides[2]):
                                    initiate_draw_edge(mainwin,i,index,color)
                                    cellid = str(i.cid).zfill(2)
                                    f="B"+f"{cellid}"+"2"
                                    break
                          elif next_click == curses.KEY_UP: 
                                index = 0     #top edge
                                if not(i.sides[0]):
                                    initiate_draw_edge(mainwin,i,index,color)
                                    cellid = str(i.cid).zfill(2)
                                    f="T"+f"{cellid}"+"0"
                                    break 
                          mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
                          mainwin.refresh()
                          break
                if(f!=''):
                     return f
                else:
                     return 0

def gameover():
     c=0
     for i in allcell:
          if(i.win != None):
                c+=1
     if(c==49):
          return 1 #gameover
     else:
        return 0 
def enter_game_player_R(mainwin,client,my_color,oppo_color):#red starts game
    mainwin.addstr(2,15,f"YOU ARE RED")
    mainwin.refresh()
    while(not gameover()):
            while(1):  #user turn
                mainwin.addstr(2,35," YOUR    TURN")
                rp = num_box_filled_red()
                gp = num_box_filled_green()
                mainwin.addstr(2,53,f"RED   PTS:{rp}")
                mainwin.addstr(3,53,f"GREEN PTS:{gp}")
                mainwin.refresh()
                rightdown.clear()
                rightdown.bkgd(" ")
                rightdown.refresh()
                rightup.clear()
                rightup.refresh()
                rightup.bkgd(" ",curses.color_pair(1)|curses.A_REVERSE)
                rightup.refresh()

                getclick = mainwin.getch()
                if getclick == curses.KEY_MOUSE:
                    _,x,y,_,_ = curses.getmouse()
                    move = inspect(x,y,mainwin,1)
                    if  move != 0:  #turn over
                        client.send(move.encode())
                        break
                    else:
                         continue 
                
            if not gameover():
                mainwin.addstr(2,35,"OPPONENT TURN")
                rp = num_box_filled_red()
                gp = num_box_filled_green()
                mainwin.addstr(2,53,f"RED   PTS:{rp}")
                mainwin.addstr(3,53,f"GREEN PTS:{gp}")
                mainwin.refresh()
                rightup.clear()
                rightup.bkgd(" ")
                rightup.refresh()
                rightdown.clear()
                rightdown.refresh()
                rightdown.bkgd(" ",curses.color_pair(2)|curses.A_REVERSE)
                rightdown.refresh()
                
                x = client.recv(1024).decode()
                if x!="121":
                    c_id = int(x[1:-1])
                    edg = int(x[-1])

                    initiate_draw_edge(mainwin,cells.give_obj_for_id(c_id),edg,oppo_color)
                else:
                    mainwin.clear()
                    mainwin.addstr(height//2,width//2 -4,"YOU WON")
                    mainwin.refresh()
                    mainwin.getch()
                    break
    mainwin.clear()
    x = display_winner(mainwin)
    if(x==my_color):
         max_wins += 1
    mainwin.getch()


def enter_game_player_G(mainwin,client,my_color,oppo_color):#green starts by follow
        mainwin.addstr(2,15,f"YOU ARE GREEN")
        mainwin.refresh()
        
        while(not gameover()):
            mainwin.addstr(2,35,"OPPONENT TURN")
            rp = num_box_filled_red()
            gp = num_box_filled_green()
            mainwin.addstr(2,53,f"RED   PTS:{rp}")
            mainwin.addstr(3,53,f"GREEN PTS:{gp}")            
            mainwin.refresh()
            rightup.clear()
            rightup.refresh()
            rightdown.clear()
            rightdown.bkgd(" ")            
            rightdown.refresh()
            rightup.bkgd(" ",curses.color_pair(1)|curses.A_REVERSE)
            rightup.refresh()
            rightdown.refresh()

            x = client.recv(1024).decode()
            if x!= "121":
                c_id = int(x[1:-1])
                edg = int(x[-1])
                initiate_draw_edge(mainwin,cells.give_obj_for_id(c_id),edg,oppo_color)
            else:
                    mainwin.clear()
                    
                    mainwin.addstr(height//2,width//2 -4,"YOU WON")
                    mainwin.refresh()
                    mainwin.getch()
                    break
            while(not gameover()):
                mainwin.addstr(2,35," YOUR    TURN")
                rp = num_box_filled_red()
                gp = num_box_filled_green()
                mainwin.addstr(2,53,f"RED   PTS:{rp}")
                mainwin.addstr(3,53,f"GREEN PTS:{gp}")                
                mainwin.refresh()              #green turn
                rightdown.clear()
                rightdown.refresh()
                rightup.clear()
                rightup.bkgd(" ") 
                rightup.refresh()
                rightdown.bkgd(" ",curses.color_pair(2)|curses.A_REVERSE)
                rightdown.refresh()
                getclick = mainwin.getch()
                if getclick == curses.KEY_MOUSE:
                    _,x,y,_,_ = curses.getmouse()
                    move = inspect(x,y,mainwin,2)
                    if  move != 0:  #turn over
                        client.send(move.encode())
                        break
                    else:
                         continue 
                else:
                     continue
                
        mainwin.clear()
        x = display_winner(mainwin)
        if(x==my_color):
              max_wins += 1
        mainwin.getch()

def draw_grid(mainwin):
        mainwin.clear()
        mainwin.refresh()
        textpad.rectangle(mainwin,0,13,32,83)
        textpad.rectangle(mainwin,1,14,31,82)
        textpad.rectangle(mainwin,0,83,16,112)
        textpad.rectangle(mainwin,0,83,32,112)

        mainwin.refresh()
        rightup.box()
        rightdown.box()
        rightup.refresh()
        rightdown.refresh()
        for col in range(8):
            for row in range(8):
                 mainwin.addstr(4+(row*3),23+(col*6),"\u2022")
                 #hexadecimal value of bullet is '0x2022'
        mainwin.refresh()


def waiting_for_oppo(mainwin,client):
    global rightdown
    global rightup

    try:
        oppo_id = client.recv(1024).decode()   #receive oppo id from global thread server of player/client
        o_color = oppo_id[-1]   #r/g
        
        if o_color == 'G':
             m_color='R'
        else:
             m_color='G'

        my_color = 2 if o_color=="R" else 1   #1/2
        opp_color = (2 if my_color == 1 else 1)   #1/2
        oppo_id = oppo_id[:-1]
        client.send(oppo_id.encode())  #send the opponent id to player's server thread
        
        rightup = mainwin.subwin(15,28,1,84)
        rightdown = mainwin.subwin(16,28,16,84)
        for  i in range(7):
             for j in range(7):
                  c = cells(i,j)
                  allcell.append(c)
        mainwin.clear()
        mainwin.refresh()
        display_rules(mainwin,m_color)
        draw_grid(mainwin)
        if my_color == 1:
        
            enter_game_player_R(mainwin,client,my_color,opp_color)
            
        else:
           enter_game_player_G(mainwin,client,my_color,opp_color)
   
    except Exception as e:
        print(e)
        mainwin.clear()
        mainwin.addstr(height//2,width//2 -4,"YOU WON")
        
        mainwin.refresh()
        mainwin.getch()
        pass


def try_to_connect(mainwin):
        global connected
        connected = False      
        while(not connected):
            try:
                for i in range(0,4):
                    dot="."*i
                    mainwin.addstr(height//2, width//2 - 14,f"CONNECTING{dot}",curses.A_BOLD | curses.color_pair(3))
                    mainwin.refresh()
                    sleep(0.3)
                    mainwin.addstr(height//2, width//2 - 14,f"CONNECTING                   ",curses.A_BOLD | curses.color_pair(3))
                    
                client = socket.socket()
                server_ip = "localhost"
                port = 56677
                client.connect((server_ip,port))
                client.send(username.encode())
                mainwin.clear()
                mainwin.refresh()
                mainwin.addstr(height//2, width//2 - 14,f"CONNECTING{dot}",curses.A_BOLD | curses.color_pair(3))
                mainwin.refresh()
                connected = True
                waiting_for_oppo(mainwin,client)
                
            except :
                if connected == 1:
                    mainwin.clear()
                    print("+")
                    mainwin.addstr(height//2,width//2 -4,"YOU WON")
                    mainwin.refresh()
                    mainwin.getch()
                    break
                else:
                     continue
                

        


def print_menu(mainwin, selected):
    mainwin.clear()
    height, width = mainwin.getmaxyx()  #no of lines
    mainwin.addstr(height//2-6, width//2 - 14,f"USE MOUSE TO SELECT / USE ARROWS TO NAVIGATE AND SELECT",curses.A_BOLD | curses.color_pair(3))
    for id, row in enumerate(menu):
        x = width // 2 - len(row) // 2
        y = height // 2 - len(menu) // 2 + id
        if id ==0:
                mainwin.addstr(y, x, row,curses.A_BOLD | curses.color_pair(2))
        elif id == selected:
            mainwin.addstr(y, x, row,curses.A_REVERSE)
        else:
            mainwin.addstr(y, x, row)
    mainwin.noutrefresh()

def print_max_wins(stats):
        stats.clear()
        stats.addstr(0,0 , f"MAX-WINS - {max_wins}",curses.A_BOLD )  #wrt stats window will be (ht_std_win - 3 , 1)
        stats.noutrefresh()

def username_reg(mainwin)->str:
        mainwin.clear()
        mainwin.addstr(height//2, width//2 - 9,"ENTER PLAYER NAME",curses.A_BOLD | curses.color_pair(3))
        mainwin.refresh()
        curses.echo()
        curses.curs_set(1)
        uname = mainwin.getstr(height//2 +3, (width//2 - 9)+2)
        curses.noecho()
        curses.curs_set(0)
        uname = uname.decode()
        while(uname)=="":
            mainwin.clear()
            mainwin.addstr(height//2, width//2 - 9,"PLAYER NAME CANNOT BE EMPTY",curses.A_BOLD | curses.color_pair(3))
            mainwin.refresh()
            curses.echo()
            uname = mainwin.getstr(height//2 +3, (width//2 - 9)+2)
            curses.noecho()
        mainwin.clear()
        mainwin.addstr(height//2 , width//2 - len(uname),f"HELLO {uname}",curses.A_BOLD | curses.color_pair(3))
        mainwin.refresh()
        return uname 

def gotomenu(mainwin,stats):
    global current_row
    curses.mousemask(1)
    curses.curs_set(0)
    
    
    print_menu(mainwin, current_row)
    print_max_wins(stats)
    
    while True:
        key = mainwin.getch()
        if key == curses.KEY_UP and current_row > 2:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            h, w = mainwin.getmaxyx()
            menu_y_start = h//2 - len(menu)//2
            if y == menu_y_start + 2 and x in range(w//2 - len(menu[2])//2, w//2 + len(menu[2])//2):
                current_row = 2
                mainwin.clear()
                mainwin.refresh()
                try_to_connect(mainwin)
            elif y == menu_y_start + 3 and x in range(w//2 - len(menu[3])//2, w//2 + len(menu[3])//2):
                current_row = 3
                exit()
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 2:
                mainwin.clear()
                mainwin.refresh()
                try_to_connect(mainwin)
            if current_row == len(menu) - 1:
                exit()
        
        print_menu(mainwin, current_row)
        print_max_wins(stats)
        curses.doupdate()



def main(mainwin):
    global height
    global width 
    global username
    global current_row
    current_row = 2
    height, width = mainwin.getmaxyx()
    stats = curses.newwin(2, 20, height - 5, 1)  #width20characters  height2line  at x,y bottom's -topleft of window =(1,h-3)   
    
    curses.curs_set(0)

    
    #to refer this call using curses.colorpair(#)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    
    mainwin.addstr(height//2 -2, width//2-len("CONNECT THE DOTS")//2,"CONNECT THE DOTS",curses.color_pair(1))
    mainwin.addstr(height//2 , width//2-len("EXPAND YOUR TERMINAL (ATLEAST lxb:35 x 130)")//2, "EXPAND YOUR TERMINAL (ATLEAST lxb:30 x 120)",curses.A_BOLD|curses.color_pair(1)) 
    mainwin.addstr(height//2 +2 , width//2-len("LOADING")//2,"LOADING",curses.color_pair(1)) 
    mainwin.refresh()
    loading = 1
    x = width//2 - 5
    while(loading != 101):
        loading+=1
        sleep(0.05)
        if(loading%10 == 0):
            x+=1
            mainwin.addstr(height//2 +4,x,"*")
            mainwin.refresh() 
    mainwin.clear()
    mainwin.refresh()
    


    username = username_reg(mainwin)
    sleep(1)

    print_menu(mainwin, current_row)
    print_max_wins(stats)
    curses.doupdate()

    gotomenu(mainwin,stats)


curses.wrapper(main)
