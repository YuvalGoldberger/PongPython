import os

class Config:
    def __init__(self):
        '''
        Sets default values for the entire game.
        '''
        self.FOLDER_LOCATION = os.getcwd()
        self.BALL_SPEED = 7
