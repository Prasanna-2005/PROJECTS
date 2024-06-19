#x,y=0,0
#mainwin.vline(y,x,'*',k)
#x,y=0,5
#mainwin.hline(y,x,ord('\u2351'),k)
import curses
from curses import textpad
from time import sleep
from curses import wrapper

allcell = []
#GRID 7 * 7   7blocks each side
# 8rows or 8lines
# 8cols or 8chars
GRID = 7
LEFT_PAD = 10 + 13 #13 outsise + 10 inside gamewindow
TOP_PAD = 4

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
                    
                    self.left = 23+(col*6)
                    self.right= self.left + 6
                    self.top = 4+(row*3)
                    self.bottom = self.top +3

                    self.sides = [0,0,0,0]  #    top,right,bottom,left

                    self.cellmid_y = (self.top + self.bottom)//2
                    self.cellmid_x = (self.left + self.right)//2

                    self.edges= [
                          [(self.left,self.top),(self.right,self.top)],  #top(0,1)
                          [(self.right,self.top),(self.right,self.bottom)],    #right  (2,3) 
                          [(self.left,self.bottom),(self.right,self.bottom)],  #bottom(4,5)
                           [(self.left,self.bottom),(self.left,self.top)],  #left  (6,7)
                          ]   


        def cellfilled(mainwin,color):  #fill cell if got 4 edges
            for i in allcell:
              if 0 not in i.sides:
                    x = curses.newwin(2,5,i.top+1,i.left+1)
                    x.bkgd(' ',curses.color_pair(1)| curses.A_REVERSE)
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
                    if edge1 in cellobj.edges :
                          ind = cellobj.edges.index(edge1)
                          cellobj.sides[ind] = 1
                    elif edge2 in cellobj.edges:
                          ind = cellobj.edges.index(edge2)
                          cellobj.sides[ind] = 1
    
                    



        def modify(self,window,color):  #red->1  green->1   draw hline and vline
             curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
             curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
             for i,side in enumerate(self.sides):
                if(side):
                        y, x = window.getyx()
                        window.attron(curses.color_pair(color))
                        if i == 0:  # top
                            window.hline(self.top, self.left, "-", 7)
                            cells.cellfilled(window,color)
                        elif i == 2:  # bottom
                            window.hline(self.bottom, self.left, "-", 7)
                            cells.cellfilled(window,color)
                        elif i == 1:  # right
                            window.vline(self.top, self.right, '|', 4)
                            cells.cellfilled(window,color)
                        elif i == 3:  # left
                            window.vline(self.top, self.left, '|', 4)
                            cells.cellfilled(window,color)
                window.attroff(curses.color_pair(color))
                window.refresh()





def draw_grid(mainwin):
        mainwin.clear()
        mainwin.refresh()
        textpad.rectangle(mainwin,0,13,32,83)
        textpad.rectangle(mainwin,1,14,31,82)
        textpad.rectangle(mainwin,0,83,16,112)
        textpad.rectangle(mainwin,0,83,32,112)
        rightup.box()
        rightdown.box()
        mainwin.refresh()
        rightup.refresh()
        rightdown.refresh()
        for col in range(8):
            for row in range(8):
                 mainwin.addstr(4+(row*3),23+(col*6),"\u2022")
                 #hexadecimal value of bullet is '0x2022'
        mainwin.refresh()
        
def inspect(x,y,mainwin):
                color = 2
                for i in allcell:
                    x_range = (i.left,i.right)
                    y_range = (i.top ,i.bottom)
                    if(x in range(x_range[0],x_range[1]+1)) and (y in range(y_range[0],y_range[1]+1)):
                          mainwin.addstr(i.cellmid_y,i.cellmid_x,".")
                          mainwin.refresh()
                          next_click = mainwin.getch()
                          if next_click == curses.KEY_LEFT:   #left edge
                                if(not i.sides[3]):
                                    mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
                                    mainwin.refresh()
                                    i.sides[3]=1
                                    i.set_edge_true(3,i.edges[3])
                                    i.modify(mainwin,color)
                                    f=1
                                    break
                          elif next_click == curses.KEY_RIGHT:    # right edge
                                if(not i.sides[1]):
                                    mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
                                    mainwin.refresh()
                                    i.sides[1]=1
                                    i.set_edge_true(1,i.edges[1])
                                    i.modify(mainwin,color)
                                    f=1
                                    break                              
                          elif next_click == curses.KEY_DOWN:    #bottom edge
                                if not(i.sides[2]):
                                    mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
                                    mainwin.refresh()
                                    i.sides[2]=1
                                    i.set_edge_true(2,i.edges[2])
                                    i.modify(mainwin,color)
                                    f=1
                                    break
                          elif next_click == curses.KEY_UP:      #top edge
                                if not(i.sides[0]):
                                    mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
                                    mainwin.refresh()
                                    i.sides[0]=1
                                    i.set_edge_true(0,i.edges[0])
                                    i.modify(mainwin,color)
                                    f=1
                                    break 
                          mainwin.addstr(i.cellmid_y,i.cellmid_x," ")
                          mainwin.refresh()
                          break
     


def main(mainwin):

        global rightdown
        global rightup
        curses.curs_set(0)
        #curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        #curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
           
        rightup = mainwin.subwin(15,28,1,84)
        rightdown = mainwin.subwin(16,28,16,84)
        

        for  i in range(7):
             for j in range(7):
                  c = cells(i,j)
                  allcell.append(c) 
        mainwin.refresh()     
        draw_grid(mainwin)
        color = 2
        mainwin.refresh()
        x=[]
        curses.mousemask(1)
        while(1):
              getclick = mainwin.getch()
              if getclick == curses.KEY_MOUSE:
                _,x,y,_,_ = curses.getmouse()
                inspect(x,y,mainwin)
                    
                            
        mainwin.refresh()
        print(x)
        mainwin.getch()
curses.wrapper(main)

