import pygame
from pygame.locals import *
import random

class Impossible:
    def __init__(self, player, ball):
        self.impossible = player
        self.ball = ball

    def moveImpossible(self):

        if self.ball.x < (pygame.display.get_surface().get_width() / 2) or self.ball.xVelocity < 0:
            return

        if self.ball.y >= self.impossible.y and self.ball.y <= self.impossible.y + self.impossible.playerHeight:
            return

        if self.ball.y < self.impossible.y:
            self.impossible.movePlayer("UP")

        elif self.ball.y > self.impossible.y - self.impossible.playerHeight:
            self.impossible.movePlayer("DOWN")

        elif self.ball.y == self.impossible.y:
            self.impossible.movePlayer("DOWN")