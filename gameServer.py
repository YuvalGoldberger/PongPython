#Server

import socket
import threading
import random
from PlayersHandlers.ball import Ball
from GameHandlers.gameManager import GameManager
import time

class server:
    def __init__(self):
        '''
        Starts server and initiates values.
        '''
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',2000))
        self.server.listen(100)
        self.gameManager = GameManager()
        self.ball = self.gameManager.ball
        self.rightPlayerX = 80
        self.leftPlayerX = 1210
        self.rightPlayerY = 360
        self.leftPlayerY = 360
        self.gameManager = GameManager()
        playersColors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))]

        self.clients=[]

        i = 0
        while True:
            client,address=self.server.accept()
            if i == 0:
                side = f"1:{playersColors[0]}:{playersColors[1]}"
            else:
                side = f"2:{playersColors[0]}:{playersColors[1]}"
            threading.Thread(target=self.clientsManager,args=(client,address, side)).start()
            i+=1
    
    def clientsManager(self,client,address, side):
        '''
        Manages client connection. Sends them the playerNum and playerColors. Also receives x,y values.
        '''
        print(address,"connected")
        self.clients.append((client,address))
        client.send(side.encode())
        numplayer = client.recv(1024).decode()

        while True:
            data = client.recv(1024).decode()
           
            if data == "startball":
                self.startBallMovement = True
                threading.Thread(target=self.moveBall).start()
            else:
                moves = data.split('---')
                for move in moves:
                    if move.split(':')[0]=='1':
                        self.rightPlayerY=float(move.split(':')[1])
                    elif move.split(':')[0]=='2':
                        self.leftPlayerY=float(move.split(':')[1])
                msg=(data).encode()
                for cl in self.clients:
                    cl[0].send(msg)
            


    def moveBall(self):
        '''
        Method being in charge of calling Ball().moveBall() and check collision.
        '''
        while True:
            status = self.gameManager.checkCollision(self.leftPlayerY, self.rightPlayerY)    
            if "SCORE" in status:
                self.startBallMovement = False
                for cl in self.clients:
                    cl[0].send(status.encode())
            if self.startBallMovement:
                self.gameManager.ball.moveBall()
                for cl in self.clients:
                    cl[0].send(f'0:{self.gameManager.ball.x}:{self.gameManager.ball.y}---'.encode()) 
                time.sleep(0.02)
            else:
                break

if __name__=='__main__':
    server()