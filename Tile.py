import pygame.sprite

import colorss
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image=pygame.Surface((size,size))
        self.rect=self.image.get_rect(topleft=(x,y))
    def update(self,shift):
        self.rect.x+=shift
class StaticTile(Tile):
    def __init__(self,size,x,y,tile_image):
        super().__init__(size,x,y)
        self.image=tile_image
class one_imageNoAnimated(StaticTile):
    def __init__(self, size, x, y,path):
        super().__init__(size, x, y,pygame.image.load(path).convert_alpha())
        y_offset=y+size
        self.rect=self.image.get_rect(bottomleft=(x,y_offset))
class AnimatedImage(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.animations=import_folder(path)

        self.frame_index=0
        self.image = self.animations[self.frame_index]
    def frames_moving(self):
        self.frame_index+=0.15
        if(self.frame_index>= len(self.animations)):
            self.frame_index=0
        self.image=self.animations[int(self.frame_index)]
    def update(self,shift):
        self.rect.x += shift
        self.frames_moving()
class Coin(AnimatedImage):
    def __init__(self, size, x, y,):
        super().__init__(size, x, y,'Graph/decoration/coin')
        self.rect=self.image.get_rect(center=(x+size/2,y+size/2))






