import socket
import threading
import time

import pygame
from pygame.locals import *

from PlayersHandlers.ball import Ball
from PlayersHandlers.player import Player

from config import Config

import socket
import threading

class GUI:
    FOLDER_LOCATION = Config().FOLDER_LOCATION
    WIDTH = 1270
    HEIGHT = 720
    

    def __init__(self):
        '''
        Initiate GUI and connect client to server.
        '''
        
        pygame.init()
        self.client= socket.socket()
        self.client.connect(('192.168.1.153',2000))

        gameData = self.client.recv(1024).decode().split(':')
 
        # eval() to turn '(1, 2, 3)' to (1, 2, 3)
        self.playerNum = gameData[0]
        self.rightPlayerColor = eval(gameData[1])
        self.leftPlayerColor = eval(gameData[2])

        print(self.playerNum)
        self.client.send(self.playerNum.encode())
        self.playerNum = int(self.playerNum)
        
        self.surface = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("Yuval - Pong Game")

        self.leftPlayerPoints = '0'
        self.rightPlayerPoints = '0'

        self.showGame()

    def showGame(self):
        '''
        Method used to control the game. Sends moves to server.
        '''

        gameFlag = True
        clock = pygame.time.Clock()
        
        self.players = Player(self.rightPlayerColor, self.leftPlayerColor)
        self.ball = Ball()

        self.players.displayBasic()
        self.ball.displayBasic()
        self.scoreDisplay()
        
        pygame.display.flip()
        i=0
        if i==0:
            threading.Thread(target=self.showScreen).start()
            i+=1

        while gameFlag:
            clock.tick(60)
            
            for event in pygame.event.get():

                if event.type == QUIT:
                    gameFlag = False

            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                if not self.ball.startBallFlag:
                    self.client.send(("startball").encode())
                    self.ball.startBallFlag = True
                
            if keys[K_UP]:
                y=self.players.movePlayer("UP", self.playerNum)
                self.client.send((str(self.playerNum)+":"+str(y)+"---").encode())

            elif keys[K_DOWN]:
                y=self.players.movePlayer("DOWN", self.playerNum)
                self.client.send((str(self.playerNum)+":"+str(y)+"---").encode())

            

    def showScreen(self):
        '''
        Displays Everything in the screen. Also recieves the moves and displays them.
        '''
        
        while True:
            self.surface.fill((0, 0, 0))

            self.scoreDisplay() 
            move = self.client.recv(1024).decode()

            try:
                moves = move.split('---')[0:-1]
                
                for move in moves:
                    if "SCORE" in move:
                        move = move.split(':')
                        self.leftPlayerPoints = move[1]
                        self.rightPlayerPoints = move[2]
                        self.ball.startBallFlag = False
                        self.players.displayBasic()
                        self.ball.displayBasic()
                    else:
                        self.players.drawPlayer(move)
                        self.ball.drawBall(move)
        
            except:
                pass

            time.sleep(0.02)      
            pygame.display.flip()

    def scoreDisplay(self):
        '''
        Displays the Score specificly. Being called in showScreen()
        '''

        scoreFont = pygame.font.Font(rf'{self.FOLDER_LOCATION}\Fonts\Assistant-ExtraBold.ttf', 50)
        pointFont = pygame.font.Font(rf'{self.FOLDER_LOCATION}\Fonts\Assistant-Medium.ttf', 30)
        scoreText = scoreFont.render("SCORE", 1, (255, 255, 255))
        leftPlayerTXT = pointFont.render(self.leftPlayerPoints.encode(), 1, (255, 255, 25))
        rightPlayerTXT = pointFont.render(self.rightPlayerPoints.encode(), 1, (255, 255, 25))

        pygame.display.get_surface().blit(scoreText, ((self.WIDTH / 2) - 75, 30 ))
        pygame.display.get_surface().blit(leftPlayerTXT, ((self.WIDTH / 2) - 150, 90 ))
        pygame.display.get_surface().blit(rightPlayerTXT, ((self.WIDTH / 2) + 150, 90 ))
    
if __name__ == '__main__':
    GUI()
