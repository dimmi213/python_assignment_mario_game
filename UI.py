import pygame

pygame.init()
class health(pygame.sprite.Sprite):
    def __init__(self):
        self.health_image = pygame.image.load('Graph/decoration/health.png').convert_alpha()
        self.health_imagex = 30
        self.health_imagey = 20
class UI:
    def __init__(self,surface):

        self.display_surface=surface
        #health
        self.health_image=pygame.image.load('Graph/decoration/health.png').convert_alpha()
        self.health_imagex=30
        self.health_imagey=20
        #coins
        self.coin_image=pygame.image.load('Graph/decoration/coin/0.png').convert_alpha()
        self.coin_image_rect=self.coin_image.get_rect(topleft=(30,60))
        self.coint_font=pygame.font.Font('Graph/decoration/font/ARCADEPI.ttf',30)

    def show_coins(self,amount):
        self.display_surface.blit(self.coin_image,self.coin_image_rect)
        coins_text=self.coint_font.render(str(amount),False,'#eae000')
        coins_textRect=coins_text.get_rect(midleft=(self.coin_image_rect.right + 8,self.coin_image_rect.centery))
        self.display_surface.blit(coins_text,coins_textRect)
    def show_health(self,health):
        if health>=0:
            for index in range(health):

                x=self.health_imagex+40*index
                self.display_surface.blit(self.health_image,(x,self.health_imagey))

