import pygame.image

from settings import *
class Background():
    def __init__(self,level_width):
        self.background1 = pygame.transform.scale(pygame.image.load('Graph/decoration/background/background_layer_1.png'),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.background2 =pygame.transform.scale(pygame.image.load('Graph/decoration/background/background_layer_2.png'),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.background3 = pygame.transform.scale(pygame.image.load('Graph/decoration/background/background_layer_3.png'),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.background11 = pygame.transform.scale(
            pygame.image.load('Graph/decoration/background/background_layer_1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background22 = pygame.transform.scale(
            pygame.image.load('Graph/decoration/background/background_layer_2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background33 = pygame.transform.scale(pygame.image.load('Graph/decoration/background/background_layer_3.png'),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.x=-400
    def draw(self,surface,shift):
            self.x+=shift
            if(self.x<=-1200):
                self.x=0

            surface.blit(self.background1,(self.x,0))
            surface.blit(self.background2, (self.x, 0))
            surface.blit(self.background3, (self.x, 0))
            surface.blit(self.background11, (self.x+1200, 0))
            surface.blit(self.background22, (self.x+1200, 0))
            surface.blit(self.background33, (self.x+1200, 0))



