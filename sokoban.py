import pygame, sys
from copy import deepcopy
from pygame.locals import *
from constants import *

setfile = open("settings.txt", 'r')
GAMESIZE = GAMESIZES[int(setfile.readline())]

WINDOWWIDTH = int(800*GAMESIZE)
WINDOWHEIGHT = int(600*GAMESIZE)
SQUARESIZE = int(50*GAMESIZE)
BOARDSIZE = 9
XLMARGIN = int((3/4*WINDOWWIDTH - BOARDSIZE*SQUARESIZE)/2)
XRMARGIN = int((3/4*WINDOWWIDTH - BOARDSIZE*SQUARESIZE)/2 + 1/4 * WINDOWWIDTH)
YMARGIN = int((3/4*WINDOWWIDTH - BOARDSIZE*SQUARESIZE)/2)
NUMBEROFLEVELS = len(LEVELS)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

ROWS = int(WINDOWWIDTH/SQUARESIZE)
COLS = int(WINDOWHEIGHT/SQUARESIZE)
pygame.init()

BASICFONT = pygame.font.Font('freesansbold.ttf', int(20*GAMESIZE))
SUBSCRIPTFONT = pygame.font.Font('freesansbold.ttf', int(15*GAMESIZE))
TITLEFONT = pygame.font.SysFont('arial', int(70*GAMESIZE))

WALL = pygame.image.load('graphics/wall.png')
WALL = pygame.transform.scale(WALL, (SQUARESIZE, SQUARESIZE))
BOX = pygame.image.load('graphics/box.png')
BOX = pygame.transform.scale(BOX, (SQUARESIZE, SQUARESIZE))
TARGET = pygame.image.load('graphics/target.png')
TARGET = pygame.transform.scale(TARGET, (SQUARESIZE, SQUARESIZE))
FLOOR = pygame.image.load('graphics/floor.png')
FLOOR = pygame.transform.scale(FLOOR, (SQUARESIZE, SQUARESIZE))
PLAYER = pygame.image.load('graphics/player.png')
PLAYER = pygame.transform.scale(PLAYER, (SQUARESIZE, SQUARESIZE))
BOXONTARGET = pygame.image.load('graphics/boxontarget.png')
BOXONTARGET = pygame.transform.scale(BOXONTARGET, (SQUARESIZE, SQUARESIZE))

def makeText(text, position, font = BASICFONT, color = DARKGRAY, bgcolor = None):
    Surf = font.render(text, 1, color, bgcolor)
    Rect = Surf.get_rect()
    Rect.center = (position[0], position[1])
    return Surf, Rect

titleSurf, titleRect = makeText('SOKOBAN', (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)), TITLEFONT)
newGameSurf, newGameRect = makeText('New Game', (int(135*GAMESIZE), int(450*GAMESIZE)), bgcolor = GRAY)
continueSurf, continueRect = makeText('Continue', (int(310*GAMESIZE), int(450*GAMESIZE)), bgcolor = GRAY)
optionsSurf, optionsRect = makeText('Options', (int(485*GAMESIZE), int(450*GAMESIZE)), bgcolor = GRAY)
bestscoresSurf, bestscoresRect = makeText('Best Scores', (int(660*GAMESIZE), int(450*GAMESIZE)), bgcolor = GRAY) 
RECTS = (newGameRect, continueRect, optionsRect, bestscoresRect)


def main():
    global DISPLAYSURF, FPSCLOCK
    
    with open('settings.txt', 'r') as file:
        data = file.readlines()
        

    isMusic = int(data[1])
    isSound = int(data[2])
    savedLevel = int(data[3])
    savedScore = int(data[4])

    pygame.mixer.pre_init(22050, -16, 2, 1)
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('sounds/background.wav')
    if isMusic == 1:
        pygame.mixer.music.play(-1, 0.0)
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('SOKOBAN')
    
    
    

    mousex = 0
    mousey = 0
    

    drawStartMenu()
    while True:
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if newGameRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (newGameRect.left-5, newGameRect.top-5, newGameRect.width + 10, newGameRect.height +10), 4)
                if mouseClicked:
                    if savedLevel == 1 or (savedLevel != 1 and confirmationBox()):
                        newGame(isMusic, isSound)
            elif continueRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (continueRect.left-5, continueRect.top-5, continueRect.width + 10, continueRect.height +10), 4)
                if mouseClicked:
                    newGame(isMusic, isSound, savedLevel, savedScore)
            elif optionsRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (optionsRect.left-5, optionsRect.top-5, optionsRect.width + 10, optionsRect.height +10), 4)
                if mouseClicked:
                    isSound = settings(isMusic, isSound)
            elif bestscoresRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (bestscoresRect.left-5, bestscoresRect.top-5, bestscoresRect.width + 10, bestscoresRect.height +10), 4)
                if mouseClicked:
                    readBestScores()
            else:
                drawStartMenu()
                    
            pygame.display.update()
            
def terminate():
    pygame.quit()
    sys.exit()


def drawStartMenu():
    DISPLAYSURF.fill(BGCOLOR)
    for i in range(ROWS):
            for j in range(COLS):
                    if i in (0, ROWS - 1) or j in (0, COLS - 1):
                            DISPLAYSURF.blit(WALL, (i*SQUARESIZE, j*SQUARESIZE))
                    else:
                            DISPLAYSURF.blit(FLOOR, (i*SQUARESIZE, j*SQUARESIZE))

    DISPLAYSURF.blit(PLAYER, (int(175*GAMESIZE), int(150*GAMESIZE)))
    DISPLAYSURF.blit(BOX, (int(375*GAMESIZE), int(150*GAMESIZE)))
    DISPLAYSURF.blit(TARGET, (int(575*GAMESIZE), int(150*GAMESIZE)))
    DISPLAYSURF.blit(titleSurf, titleRect)
    DISPLAYSURF.blit(newGameSurf, newGameRect, )
    DISPLAYSURF.blit(continueSurf, continueRect)
    DISPLAYSURF.blit(optionsSurf, optionsRect)
    DISPLAYSURF.blit(bestscoresSurf, bestscoresRect)    
    pygame.display.update()

def readBestScores():
    with open('highscores.txt', 'r') as file:
        data = file.readlines()
    display = True
    k = 0
    DISPLAYSURF.fill(GRAY)
    scoreSurf, scoreRect = makeText('BEST SCORES', (int(WINDOWWIDTH/2), int((100+k*50)*GAMESIZE)), BASICFONT, color = BROWN)
    DISPLAYSURF.blit(scoreSurf, scoreRect)  
    for d in data:
        k += 1
        surf, rect = makeText(d[:-1], (int(WINDOWWIDTH/2), int((100+k*50)*GAMESIZE)), BASICFONT, color = BROWN)
        DISPLAYSURF.blit(surf, rect)
    k += 1
    surf, rect = makeText('BACK', (int(WINDOWWIDTH/2), int((100+k*50)*GAMESIZE)), BASICFONT)
    DISPLAYSURF.blit(surf, rect)
    
    pygame.display.update()
    while display:
        mouseClicked = False
        for event in pygame.event.get():
            pygame.draw.rect(DISPLAYSURF, GRAY, (rect.left-5, rect.top-5, rect.width + 10, rect.height +10), 4)
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if rect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (rect.left-5, rect.top-5, rect.width + 10, rect.height +10), 4)
                if mouseClicked:
                    display = False
            pygame.display.update()

def settings(isMusic, isSound):
    mousex = 0
    mousey = 0
    display = True
    

    aSurf, aRect, bSurf, bRect, cSurf, cRect = checkSettings('settings.txt')
    dSurf, dRect = makeText('BACK', (int(WINDOWWIDTH/2), int(500*GAMESIZE)), BASICFONT, color = DARKGRAY)
    eSurf, eRect = makeText('Change in resolution will be applied after game restart', (int(WINDOWWIDTH/2), int(250*GAMESIZE)), SUBSCRIPTFONT, color = BROWN)

    drawSettings(aSurf, aRect, bSurf, bRect, cSurf, cRect, dSurf, dRect, eSurf, eRect)
    while display:
        
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if aRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (aRect.left-5, aRect.top-5, aRect.width + 10, aRect.height +10), 4)
                if mouseClicked:
                    isSound = switchSettings(0, 3)
            elif bRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (bRect.left-5, bRect.top-5, bRect.width + 10, bRect.height +10), 4)
                if mouseClicked:
                    isSound = switchSettings(1, 2, isMusic)
            elif cRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (cRect.left-5, cRect.top-5, cRect.width + 10, cRect.height +10), 4)
                if mouseClicked:
                    isSound = switchSettings(2, 2, isSound)
                      
            elif dRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (dRect.left-5, dRect.top-5, dRect.width + 10, dRect.height +10), 4)
                if mouseClicked:
                    display = False
            else:
                aSurf, aRect, bSurf, bRect, cSurf, cRect = checkSettings('settings.txt')
                drawSettings(aSurf, aRect, bSurf, bRect, cSurf, cRect, dSurf, dRect, eSurf, eRect)
                
            pygame.display.update()  
                  
    return isSound
                

def checkSettings(data):
    with open(data, 'r') as file:
        d = file.readlines()
    k = 1
    if int(d[0]) == 0:
        aSurf, aRect = makeText('RESOLUTION: 640 x 480', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    elif int(d[0]) == 1:
        aSurf, aRect = makeText('RESOLUTION: 800 x 600', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    elif int(d[0]) == 2:
        aSurf, aRect = makeText('RESOLUTION: 1200 x 900', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    k += 1
    if int(d[1]) == 0:
        bSurf, bRect = makeText('MUSIC: OFF', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    if int(d[1]) == 1:
        bSurf, bRect = makeText('MUSIC: ON', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    k += 1
    if int(d[2]) == 0:
        cSurf, cRect = makeText('SOUND EFFECTS: OFF', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    if int(d[2]) == 1:
        cSurf, cRect = makeText('SOUND EFFECTS: ON', (int(WINDOWWIDTH/2), int((100+k*100)*GAMESIZE)), BASICFONT, color = BROWN, bgcolor = SILVER)
    return aSurf, aRect, bSurf, bRect, cSurf, cRect

def drawSettings(aSurf, aRect, bSurf, bRect, cSurf, cRect, dSurf, dRect, eSurf, eRect):
    DISPLAYSURF.fill(GRAY)
    optSurf, optRect = makeText('SETTINGS', (int(WINDOWWIDTH/2), int(100*GAMESIZE)), BASICFONT, color = BROWN)
    DISPLAYSURF.blit(optSurf, optRect)
    DISPLAYSURF.blit(aSurf, aRect)
    DISPLAYSURF.blit(bSurf, bRect)
    DISPLAYSURF.blit(cSurf, cRect)
    DISPLAYSURF.blit(dSurf, dRect)
    DISPLAYSURF.blit(eSurf, eRect)
    pygame.display.update()

def switchSettings(line, pos, isMusic = None, isSound = None):
    with open('settings.txt', 'r') as file:
        data = file.readlines()
        data[line] = str((int(data[line])+1)%pos)+'\n'
    with open('settings.txt', W) as file:
        file.writelines( data )
    if line == 1:
        isMusic = int(data[line])
        if isMusic == 1:
            pygame.mixer.music.play(-1, 0.0)
        else:
            pygame.mixer.music.stop()
    if line == 2:
        isSound = int(data[line])
    return isSound

def confirmationBox():
    ySurf, yRect = makeText('YES', (int(300*GAMESIZE), int(400*GAMESIZE)), BASICFONT, color = BROWN)
    nSurf, nRect = makeText('NO', (int(500*GAMESIZE), int(400*GAMESIZE)), BASICFONT, color = BROWN)
    drawBox(ySurf, yRect, nSurf, nRect)
    display = True
    newGame = False
    mousex = 0
    mousey = 0
    while display:
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if yRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (yRect.left-5, yRect.top-5, yRect.width + 10, yRect.height +10), 4)
                if mouseClicked:
                    display = False
                    newGame = True 
            elif nRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (nRect.left-5, nRect.top-5, nRect.width + 10, nRect.height +10), 4)
                if mouseClicked:
                    display = False
                    newGame = False        
            else:
                aSurf, aRect, bSurf, bRect, cSurf, cRect = checkSettings('settings.txt')
                drawBox(ySurf, yRect, nSurf, nRect)
                
            pygame.display.update()  
    return newGame
        

def drawBox(ySurf, yRect, nSurf, nRect):
    DISPLAYSURF.fill(GRAY)
    surf, rect = makeText('Starting new game will erase your save. Proceed?', (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)), BASICFONT, color = BROWN)
    DISPLAYSURF.blit(surf, rect)
    DISPLAYSURF.blit(ySurf, yRect)
    DISPLAYSURF.blit(nSurf, nRect)
    pygame.display.update()


def newGame(isMusic, isSound, level = 1, score = 0):

    if level == 1:
        autoSave(0, 1)
        
    lvl = deepcopy(LEVELS[level-1])
    sc = score
    soundFanfare = pygame.mixer.Sound('sounds/fanfare.wav')

    resetSurf, resetRect = makeText('RESET LEVEL', (int((WINDOWWIDTH - XRMARGIN)+XRMARGIN/2), int(3/4*WINDOWHEIGHT)), BASICFONT)
    
    drawBoard(level - 1, sc, resetSurf, resetRect)
    drawBoardState(lvl)

    
    
    while True:
        for event in pygame.event.get():
            mouseClicked = False
            mousex = 0
            mousey = 0
            
            if event.type == QUIT:
                terminate()
                
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if resetRect.collidepoint(mousex, mousey):
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, (resetRect.left-5, resetRect.top-5, resetRect.width + 10, resetRect.height +10), 4)
                if mouseClicked:
                    newGame(isMusic, isSound, level, score)
                    return
                    
            if event.type == KEYDOWN:
                px, py = getPlayerPosition(lvl)
                if event.key == K_ESCAPE:
                    isSound = settings(isMusic, isSound)
                if event.key in (K_w, K_UP):
                    if validMove(lvl, UP, px, py, isSound) == 1:
                        lvl, sc = updateBoardState(lvl, LEVELS[level-1], UP, px, py), sc + 1
                    elif validMove(lvl, UP, px, py, isSound) == 2:
                        lvl, sc = updateBoardState(lvl, LEVELS[level-1], UP, px, py, True), sc + 1
                elif event.key in (K_s, K_DOWN):
                    if validMove(lvl, DOWN, px, py, isSound) == 1:
                        lvl, sc  = updateBoardState(lvl, LEVELS[level-1], DOWN, px, py), sc + 1
                    elif validMove(lvl, DOWN, px, py, isSound) == 2:
                        lvl, sc  = updateBoardState(lvl, LEVELS[level-1], DOWN, px, py, True), sc + 1
                elif event.key in (K_d, K_RIGHT):
                    if validMove(lvl, RIGHT, px, py, isSound) == 1:
                        lvl, sc  = updateBoardState(lvl, LEVELS[level-1], RIGHT, px, py), sc + 1
                    elif validMove(lvl, RIGHT, px, py, isSound) == 2:
                        lvl, sc  = updateBoardState(lvl, LEVELS[level-1], RIGHT, px, py, True), sc + 1
                elif event.key in (K_a, K_LEFT):   
                    if validMove(lvl, LEFT, px, py, isSound) == 1:
                        lvl, sc  = updateBoardState(lvl, LEVELS[level-1], LEFT, px, py), sc + 1
                    elif validMove(lvl, LEFT, px, py, isSound) == 2:
                        lvl, sc  = updateBoardState(lvl, LEVELS[level-1], LEFT, px, py, True), sc + 1
                drawBoard(level - 1, sc, resetSurf, resetRect)
                drawBoardState(lvl)

        if checkSolution(lvl):
            if isSound == 1:
                soundFanfare.play()
            pygame.time.delay(4000)
            if level < NUMBEROFLEVELS:
                autoSave(sc)
                newGame(isMusic, isSound, level+1, sc)
            else:
                highscore = False
                with open('highscores.txt', 'r') as file:
                    data = file.readlines()
                    
                for line in range(len(data)):
                    data[line] = int(data[line])
                    
                data.append(sc)
                data.sort()
                if data[len(data)-1] != sc:
                    highscore = True
                data = data[:-1]
                for line in range(len(data)):
                    data[line] = str(data[line])+'\n'
                
                with open('highscores.txt', W) as file:
                    file.writelines( data )

                display = True
                mouseClicked = False
                mousex = 0
                mousey = 0
                surf, rect = makeText('BACK', (int(WINDOWWIDTH/2), int(7/8*WINDOWHEIGHT)), BASICFONT)
                drawFinal(highscore, sc, surf, rect)
                while display:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            terminate()
                        if event.type == MOUSEMOTION:
                            mousex, mousey = event.pos
                        elif event.type == MOUSEBUTTONUP:
                            mousex, mousey = event.pos
                            mouseClicked = True
                    if rect.collidepoint(mousex, mousey):
                        pygame.draw.rect(DISPLAYSURF, DARKGRAY, (rect.left-5, rect.top-5, rect.width + 10, rect.height +10), 4)
                        if mouseClicked:
                            display = False
                    pygame.display.update()
                

                
        if checkSolution(lvl):
            return
                
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)
            
def drawFinal(highscore, sc, surf, rect):

    DISPLAYSURF.fill(GRAY)
    conSurf, conRect = makeText('CONGRATULATIONS!!!', (int(WINDOWWIDTH/2), int(1/8*WINDOWHEIGHT)), TITLEFONT)
    descSurf, descRect = makeText('You have solved all of the puzzles!', (int(WINDOWWIDTH/2), conRect.bottom + SQUARESIZE), BASICFONT)
    desc2Surf, desc2Rect = makeText('Your score of:', (int(WINDOWWIDTH/2), descRect.bottom + SQUARESIZE), BASICFONT)
    scString = str(sc) + ' total moves'
    scSurf, scRect = makeText(scString, (int(WINDOWWIDTH/2), desc2Rect.bottom + 2 * SQUARESIZE), TITLEFONT)
    if highscore:
        hsString = 'is good enough to be put on a highscores list! Great Job!!!'
    else:
        hsString = 'is not good enough to be put on a highscores list. Try again!'
    hsSurf, hsRect = makeText(hsString, (int(WINDOWWIDTH/2), scRect.bottom + 2 * SQUARESIZE), BASICFONT)
    DISPLAYSURF.blit(conSurf, conRect)
    DISPLAYSURF.blit(descSurf, descRect)
    DISPLAYSURF.blit(desc2Surf, desc2Rect)
    DISPLAYSURF.blit(scSurf, scRect)
    DISPLAYSURF.blit(hsSurf, hsRect)
    DISPLAYSURF.blit(surf, rect)
    pygame.display.update()
                                                    

def drawBoard(level, score, resetSurf, resetRect):
    board = LEVELS[level]
    DISPLAYSURF.fill(BGCOLOR)
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]:
                if board[i][j] == W:
                    DISPLAYSURF.blit(WALL, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
                else:
                    DISPLAYSURF.blit(FLOOR, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
    lSurf, lRect = makeText('LEVEL: ' + str(level+1), (int((WINDOWWIDTH - XRMARGIN) + XRMARGIN/2), int(1/4*WINDOWHEIGHT)), BASICFONT)
    sSurf, sRect = makeText('TOTAL MOVES: ' + str(score), (int((WINDOWWIDTH - XRMARGIN)+XRMARGIN/2), int(1/2*WINDOWHEIGHT)), BASICFONT)
    DISPLAYSURF. blit(lSurf, lRect)
    DISPLAYSURF. blit(sSurf, sRect)
    DISPLAYSURF. blit(resetSurf, resetRect)
    pygame.display.update()

def drawBoardState(lvl):
    for i in range(len(lvl)):
        for j in range(len(lvl[0])):
            if lvl[i][j]:
                if lvl[i][j] == P:
                    DISPLAYSURF.blit(PLAYER, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
                elif lvl[i][j] == B:
                    DISPLAYSURF.blit(BOX, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
                elif lvl[i][j] == T:
                    DISPLAYSURF.blit(TARGET, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
                elif lvl[i][j] == K:
                    DISPLAYSURF.blit(BOXONTARGET, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
                elif lvl[i][j] == M:
                    DISPLAYSURF.blit(TARGET, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
                    DISPLAYSURF.blit(PLAYER, (XLMARGIN + i*SQUARESIZE, YMARGIN + j*SQUARESIZE))
    pygame.display.update()
    
def getPlayerPosition(lvl):
    for x in range(len(lvl)):
        for y in range(len(lvl)):
            if lvl[x][y] == P or lvl[x][y] == M:
                return (x,y)

def validMove(lvl, direction, px, py, isSound):
    k = None
    soundStep = pygame.mixer.Sound('sounds/step2.wav')
    soundPush = pygame.mixer.Sound('sounds/push2.wav')
    
    if direction == UP:
        if lvl[px][py-1] in (F, T):
            k = 1
        elif lvl[px][py-1] in (B, K) and lvl[px][py-2] in (F, T):
            k = 2
    elif direction == DOWN:
        if lvl[px][py+1] in (F, T):
            k = 1
        elif lvl[px][py+1] in (B, K) and lvl[px][py+2] in (F, T):
            k = 2
    elif direction == RIGHT:
        if lvl[px+1][py] in (F, T):
            k = 1
        elif lvl[px+1][py] in (B, K) and lvl[px+2][py] in (F, T):
            k = 2
    elif direction == LEFT:
        if lvl[px-1][py] in (F, T):
            k = 1
        elif lvl[px-1][py] in (B, K) and lvl[px-2][py] in (F, T):
            k = 2
    if k == 1 and isSound == 1:
        soundStep.play()
    if k == 2 and isSound == 1:
        soundPush.play()
    return k

def updateBoardState(lvl, default, direction, px, py, push = False):
    if direction == UP:
        if default[px][py-1] in (T, K):
            lvl[px][py-1] = M
        else:
            lvl[px][py-1] = P
        if default[px][py] in (B, F, P):    
            lvl[px][py] = F
        else:
            lvl[px][py] = T
        if push:
            if default[px][py-2] in (T, K):
                lvl[px][py-2] = K
            else:
                lvl[px][py-2] = B
    elif direction == DOWN:
        if default[px][py+1] in (T, K):
            lvl[px][py+1] = M
        else:
            lvl[px][py+1] = P
        if default[px][py] in (B, F, P):
            lvl[px][py] = F
        else:
            lvl[px][py] = T
        if push:
            if default[px][py+2] in (T, K):
                lvl[px][py+2] = K
            else:
                lvl[px][py+2] = B
    elif direction == RIGHT:
        if default[px+1][py] in (T, K):
            lvl[px+1][py] = M
        else:
            lvl[px+1][py] = P
        if default[px][py] in (B, F, P):
            lvl[px][py] = F
        else:
            lvl[px][py] = T
        if push:
            if default[px+2][py] in (T, K):
                lvl[px+2][py] = K
            else:
                lvl[px+2][py] = B    
    elif direction == LEFT:
        if default[px-1][py] in (T, K):
            lvl[px-1][py] = M
        else:
            lvl[px-1][py] = P
        if default[px][py] in (B, F, P):
            lvl[px][py] = F
        else:
            lvl[px][py] = T
        if push:
            if default[px-2][py] in (T, K):
                lvl[px-2][py] = K
            else:
                lvl[px-2][py] = B
    return lvl

def checkSolution(lvl):
    for i in range(len(lvl)):
        for j in range(len(lvl)):
            if lvl[i][j] == 'b':
                return False
    return True

def autoSave(sc, level = 0):
    with open('settings.txt', 'r') as file:
        data = file.readlines()
    if level == 0:
        data[3] = str(int(data[3])+1)+ '\n'
        data[4] = str(sc)+ '\n'
    else:
        data[3] = str(1) + '\n'
        data[4] = str(0) + '\n'
    with open('settings.txt', W) as file:
        file.writelines( data )

if __name__ == '__main__':
    main()
