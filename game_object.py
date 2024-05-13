import pygame
from setting import *
import pygame
import time
import random
import math

bullet_image = pygame.image.load("images/Meteorit.png")

class Bullet:
    def __init__(self, x, y, speed, source):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = speed
        self.source = source

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 4, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class BossLvl3Bullet(Bullet):
    def __init__(self, x, y, speed, image):
        super().__init__(x, y, speed, "boss_lvl3")
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 0
        self.max_lifetime = 60

    def update(self):
        super().update()
        self.lifetime += 1
        if self.lifetime > self.max_lifetime:
            self.remove()

    def remove(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
