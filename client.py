from gui import GUI
import socket
from pygame.locals import *

class Client:

    def __init__(self):
        self.client = socket.socket()
        self.client.connect(('192.168.1.153', 12345))
        gui = GUI()

        while True:
            data = self.client.recv(1024).decode()
            if data == "SHOW":
                gui.showScreen()