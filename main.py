import pygame
from pygame.locals import *

from GameHandlers.button import Button
from GameHandlers.gameManager import GameManager

from Sockets.server import Server


class GUI:

    def __init__(self):
        pygame.init()
        
        WIDTH = 1270
        HEIGHT = 720
        self.surface = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Yuval - Pong Game")

        gameFlag = True
        madeByFlag = False
        #  Modes can be "AI", "MultiPlayer", "Impossible"
        selectedMode = ""
        
        clock = pygame.time.Clock()
    
        gameManager = GameManager()
        firstPlayer = gameManager.firstPlayer
        secondPlayer = gameManager.secondPlayer
        ball = gameManager.ball
        impossiblePlayer = gameManager.impossiblePlayer

        buttonMultiPlayer = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\MultiPlayer.png',
                                     WIDTH / 2 + 100, HEIGHT / 2 + 100)
        buttonAI = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\playWithAI.png', 
                            WIDTH / 2 - 100, HEIGHT / 2 + 200)
        buttonImpossible = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\Impossible.png', 
                            WIDTH / 2 - 300, HEIGHT / 2 + 100)  

        
        pygame.display.flip()
        while gameFlag:
            clock.tick(60)
            for event in pygame.event.get():

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    cursorX, cursorY = pygame.mouse.get_pos()
                    buttonImpossible.checkPressed(cursorX, cursorY)
                    if buttonImpossible.checkPressed(cursorX, cursorY):
                        selectedMode = "Impossible"
                        gameManager.resetScore()
                    elif buttonMultiPlayer.checkPressed(cursorX, cursorY):
                        selectedMode = "MultiPlayer"
                        gameManager.resetScore()
                    elif buttonAI.checkPressed(cursorX, cursorY):
                        selectedMode = "AI" 
                        gameManager.resetScore()

                if event.type == QUIT:
                    gameFlag = False

            keys = pygame.key.get_pressed()

            if keys[K_RETURN]:
                ball.startBall()
                madeByFlag = True
            if keys[K_w]:
                firstPlayer.movePlayer("UP")
            elif keys[K_s]:
                firstPlayer.movePlayer("DOWN")
            if selectedMode == "MultiPlayer":
                if keys[K_UP]:
                    secondPlayer.movePlayer("UP")
                elif keys[K_DOWN]:
                    secondPlayer.movePlayer("DOWN")        

            self.surface.fill((0, 0, 0))

            #  Check if game started, if not move the ball
            if ball.startBallFlag:
                ball.moveBall()
            #  If game did not start, show "Press Enter to start"
            if not ball.startBallFlag:
                gameManager.startingGameAlert()
                buttonMultiPlayer.displayButton()     
                buttonAI.displayButton()           
                buttonImpossible.displayButton()
                #  Only for the first time, show "Made By Yuval"
                if not madeByFlag:
                    gameManager.madeByDisplay()
            #  After first time, show score (and not "Made by Yuval")
            if madeByFlag:
                gameManager.scoreDisplay()
            if selectedMode == "AI":
                buttonAI.displayState(selectedMode)
            elif selectedMode == "MultiPlayer":
                buttonMultiPlayer.displayState(selectedMode)
            elif selectedMode == "Impossible":
                buttonImpossible.displayState(selectedMode)
            if selectedMode == "Impossible":
                impossiblePlayer.moveImpossible()
            gameManager.checkCollision()
            ball.drawBall()
            firstPlayer.drawPlayer()
            secondPlayer.drawPlayer()
            
            pygame.display.flip()


GUI()