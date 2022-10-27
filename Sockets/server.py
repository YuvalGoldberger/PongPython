import socket
import threading

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