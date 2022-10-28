import socket
import threading
from gui import GUI
import pygame
from pygame.locals import *

class Server:

    PORT = 12345

    def __init__(self):
        self.server = socket.socket()

        self.server.bind(("0.0.0.0", self.PORT))
        self.server.listen(100)
        print("waiting..")
            
        for i in range(10):
            threading.Thread(target=self.clientHandler).start()
            

    def clientHandler(self, client, address):
        client, address = self.server.accept()
        clientList = []
        playersInMatch = []
        print(address, " has been connected!")
        if len(clientList) == 2:
            playersInMatch += clientList
            clientList = []
        if len(playersInMatch == 2):
            self.match(playersInMatch)
            playersInMatch = []
            
        else:
            clientList.append(client)
        while True:
            try:
                msg = client.recv(1024).decode()
                if msg == "/exit":
                    clientList.remove(client)
                    client.close()
                    break

                for conn in clientList:
                    if conn != client:
                        conn.send(f'{address} sent: {msg}'.encode())
                    else:
                        client.send(f'You sent: {msg}'.encode())
            except:
                break

    def match(self, playersList):
        gui = GUI()
        data = pygame.image.tostring(gui.image, "RGB")
        while True:
            for player in playersList:
                player.send(data)


        pass