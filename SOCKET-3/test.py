#x,y=0,0
#mainwin.vline(y,x,'*',k)
#x,y=0,5
#mainwin.hline(y,x,ord('\u2351'),k)
import curses as c
from curses import textpad
from time import sleep
import random
from curses import wrapper
def main(mainwin):
   y,x =mainwin.getmaxyx()
   print(x,y)
   c.mousemask(c.ALL_MOUSE_EVENTS)
   gamewin = c.newwin(33,100,0,13)
   rightup = gamewin.subwin(16,28,1,83)
   rightdown = gamewin.subwin(17,30,17,83)
   mainwin.refresh()
   gamewin.box()
   rightup.box()
   rightdown.box()
   gamewin.refresh() 
   rightup.refresh()
   gamewin.refresh()
   
   for col in range(8):
            for row in range(8):
                 gamewin.addstr(4+(row*3),10+(col*6),"\u2022")
                 gamewin.refresh()

   c.init_pair(1, c.COLOR_RED, c.COLOR_BLACK)
   c.init_pair(2, c.COLOR_GREEN, c.COLOR_BLACK)
   while True:
       gamewin.refresh()
       L=[(0,0),(3,2),(2,3),(4,5),(6,5)]
       random.shuffle(L)
       print(L)
       for i in range(5):
          x = random.choice(L)
          row = x[0]
          col = x[1]
          L.remove(x)
          gamewin.attron(c.color_pair((i%2)+1))
          gamewin.hline(4+(row*3),10+(col*6),"-",7)
          gamewin.vline(4+(row*3),10+(col*6),"|",4)
          gamewin.attroff(c.color_pair((i%2)+1))
       gamewin.refresh()
       mainwin.getch()
       break
c.wrapper(main)