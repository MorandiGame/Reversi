import pygame
from pygame.locals import *
from copy import copy

# Predetermined parameters
BOARDSIZE,BLOCKSIZE,TOPHEIGHT,BOTTOMHEIGHT = 8,60,100,100
BOARDLENGTH = BOARDSIZE * BLOCKSIZE
RADIUS,SMALLRADIUS,CIRCLEWIDTH = 24,14,6
BUTTONWIDTH,BUTTONHEIGHT = 120,36
TITLEPOSITION = (160,33)
BUTTONPOSITION = list(((36 + int(x * 2.5 * BLOCKSIZE),
 TOPHEIGHT + BOARDSIZE * BLOCKSIZE + (BOTTOMHEIGHT - BUTTONHEIGHT) // 2)
                       for x in range(3)))
WORDPOSITIONX,WORDPOSITIONY = (30,32,43),15
WORDPOSITION=list((((BUTTONPOSITION[x][0]+BUTTONWIDTH//2-WORDPOSITIONX[x]),
  TOPHEIGHT + BOARDSIZE * BLOCKSIZE + BOTTOMHEIGHT // 2 - WORDPOSITIONY)
                   for x in range(3)))
TITLE = 'REVERSI'
WORD = ('Start','Undo','Options')
ENDGAMEPOSITION = (0,0)
FONT,FONTSIZE = {'TITLE':'castellar','WORD':'century'},{'TITLE':36,'WORD':24}
COLOR = {'BACKGROUND':(204,204,102),1:(0,0,0),2:(255,255,255),
         'TOP':(102,51,0),'BOTTOM':(204,153,102),'LINE':(102,102,0),
         'TITLE':(255,255,102),'WORD':(102,51,0),'ENDGAME':(153,153,153),
         'BUTTON':(153,255,153)}

# Optional Parameters
Hint = True
Computer = False
Difficulty = 0
Train = False

class Reversi:
    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((BOARDLENGTH,
                        BOARDLENGTH + TOPHEIGHT + BOTTOMHEIGHT))
        pygame.display.set_caption(TITLE)
        self.titlefont=pygame.font.SysFont(FONT['TITLE'],FONTSIZE['TITLE'])
        self.wordfont = pygame.font.SysFont(FONT['WORD'],FONTSIZE['WORD'])
        self.drawinitboard()
        self.starts = 0
        self.gamestate = 'Init'
        self.history = []

    def start(self):
        self.screen.fill(COLOR['BACKGROUND'])
        self.drawinitboard()
        self.gamestate = 'Ongoing'
        self.starts += 1
        self.history = []
        s = BOARDSIZE
        self.board = [[0 for x in range(s)] for y in range(s)]
        self.total,self.state = 4,1
        # 1 stands for black and 2 stands for white
        self.board[s//2][s//2],self.board[s//2-1][s//2-1] = 2,2
        self.board[s//2-1][s//2],self.board[s//2][s//2-1] = 1,1
        
    def click(self,x,y):
        if not (x>=0 and x < BOARDSIZE and y>=0 and y < BOARDSIZE):return
        availlist = self.avail(x,y,self.state)
        if len(availlist) == 0 : return 
        for m in availlist: self.board[m[0]][m[1]] = self.state
        self.board[x][y] = self.state
        self.history.append((x,y))
        self.total += 1
        if self.total==BOARDSIZE**2 or self.score()[1]*self.score()[2]==0:
            self.endgame()
            return
        for m in [(x,y)for x in range(BOARDSIZE) for y in range(BOARDSIZE)]:
            if len(self.avail(m[0],m[1],3-self.state)) != 0 :
                self.state = 3 - self.state
                break
        else:
            for m in [(x,y)for x in range(BOARDSIZE) for y in range(BOARDSIZE)]:
                if len(self.avail(m[0],m[1],self.state)) != 0:
                    break
            else: self.endgame()
                

    def score(self): 
        a=len([0 for x in range(BOARDSIZE) for y in range(BOARDSIZE)
               if self.board[x][y] == 1])
        b=len([0 for x in range(BOARDSIZE) for y in range(BOARDSIZE)
               if self.board[x][y] == 2])
        return (a + b,a,b)

    def endgame(self):
        a = ('GameOver!Black'+str(self.score()[1])
            +'White'+str(self.score()[2]))
        printing = self.wordfont.render(a,True,COLOR['ENDGAME'])
        self.screen.blit(printing,ENDGAMEPOSITION)
        self.gamestate = 'End'
        pygame.display.flip()

    def drawinitboard(self):
        self.screen.fill(COLOR['BACKGROUND'])
        pygame.draw.rect(self.screen,COLOR['TOP'],pygame.Rect
            (0,0,BOARDSIZE * BLOCKSIZE,TOPHEIGHT))
        pygame.draw.rect(self.screen,COLOR['BOTTOM'],pygame.Rect
            (0,TOPHEIGHT + BOARDLENGTH,BOARDLENGTH,BOTTOMHEIGHT))
        for x in range(3):
          pygame.draw.rect(self.screen,COLOR['BUTTON'],pygame.Rect
            (BUTTONPOSITION[x][0],BUTTONPOSITION[x][1],
             BUTTONWIDTH,BUTTONHEIGHT))
        title = self.titlefont.render(TITLE,True,COLOR['TITLE'])
        self.screen.blit(title,TITLEPOSITION)
        word = [0,0,0]
        for x in range(3):
            word[x] = self.wordfont.render(WORD[x],True,COLOR['WORD'])
            self.screen.blit(word[x],WORDPOSITION[x])
        for x in range(BOARDSIZE + 1):
            pygame.draw.line(self.screen,COLOR['LINE'],
                        (0,x * BLOCKSIZE + TOPHEIGHT),
                        (BOARDLENGTH,x * BLOCKSIZE + TOPHEIGHT))
            pygame.draw.line(self.screen,COLOR['LINE'],
                        (x * BLOCKSIZE,TOPHEIGHT),
                        (x * BLOCKSIZE,BOARDLENGTH + TOPHEIGHT))
        pygame.display.flip()
        
    def drawboard(self):
        pygame.draw.rect(self.screen,COLOR['BACKGROUND'],
                pygame.Rect(0,TOPHEIGHT,BOARDLENGTH,BOARDLENGTH))
        for x in range(BOARDSIZE + 1):
            pygame.draw.line(self.screen,COLOR['LINE'],
                        (0,x * BLOCKSIZE + TOPHEIGHT),
                        (BOARDLENGTH,x * BLOCKSIZE + TOPHEIGHT))
            pygame.draw.line(self.screen,COLOR['LINE'],
                        (x * BLOCKSIZE,TOPHEIGHT),
                        (x * BLOCKSIZE,BOARDLENGTH + TOPHEIGHT))
        for x in range(BOARDSIZE):
            for y in range(BOARDSIZE):
                if self.board[x][y] != 0:
                    pygame.draw.circle(self.screen,COLOR[self.board[x][y]],
                        (int((x + 1/2) * BLOCKSIZE),
                         int((y + 1/2) * BLOCKSIZE) + TOPHEIGHT),RADIUS)
        if Hint == True :
            allowedlist = []
            for x in range(BOARDSIZE):
                for y in range(BOARDSIZE):
                    if len(self.avail(x,y,self.state)) > 0:
                        allowedlist.append((x,y))
            for m in allowedlist:
                pygame.draw.circle(self.screen,COLOR[self.state],
                        (int((m[0] + 1/2) * BLOCKSIZE),
                        int((m[1] + 1/2) * BLOCKSIZE) + TOPHEIGHT),
                        SMALLRADIUS,CIRCLEWIDTH)
        pygame.display.flip()

    def avail(self,x,y,state): 
        if self.board[x][y]!=0 : return []
        winlist = []
        def judge(coorlist): 
            list = [self.board[m[0]][m[1]] for m in coorlist]
            try: i = list.index(state)
            except ValueError: return
            for x in range(i):
                if list[x] != 3 - state: return
            else: winlist.extend(coorlist[:i])
        judge([(x,y + t) for t in range(1,BOARDSIZE) if y + t < BOARDSIZE])
        judge([(x,y - t) for t in range(1,BOARDSIZE) if y - t >= 0])
        judge([(x + t,y) for t in range(1,BOARDSIZE) if x + t < BOARDSIZE])
        judge([(x - t,y) for t in range(1,BOARDSIZE) if x - t >= 0])
        judge([(x + t,y + t) for t in range(1,BOARDSIZE) 
                            if x + t < BOARDSIZE and y + t < BOARDSIZE])
        judge([(x - t,y - t) for t in range(1,BOARDSIZE) 
                            if x - t >= 0 and y - t >= 0])
        judge([(x + t,y - t) for t in range(1,BOARDSIZE) 
                            if x + t < BOARDSIZE and y - t >= 0])
        judge([(x - t,y + t) for t in range(1,BOARDSIZE) 
                            if x - t >= 0 and y + t < BOARDSIZE])
        return winlist  # returning the list of all reversed pieces

    def undo(self):
        self.history.pop()
        temp = copy(self.history)
        self.drawinitboard()
        self.start()
        self.starts -= 1
        for m in temp:
            self.click(m[0],m[1])
        self.drawboard()

    def options(self):
        pass

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == MOUSEBUTTONUP :
                    x,y,b = event.pos[0],event.pos[1],BUTTONPOSITION
                    if (y > BOTTOMHEIGHT and
                        y <= TOPHEIGHT + BOARDLENGTH and
                        self.gamestate == 'Ongoing'):
                            self.click(x//BLOCKSIZE,
                                       (y-TOPHEIGHT)//BLOCKSIZE)
                            self.drawboard()
                    if y > b[0][1] and y < b[0][1] + BUTTONHEIGHT:
                        if x > b[0][0] and x < b[0][0] + BUTTONWIDTH:
                            self.start()
                            self.drawboard()
                        elif x > b[1][0] and x < b[1][0] + BUTTONWIDTH:
                            if len(self.history) > 0 :
                                self.undo()
                        elif x > b[2][0] and x < b[2][0] + BUTTONWIDTH:
                            self.options()

def play():
    Reversi().play()

if __name__ == '__main__':
    play()
