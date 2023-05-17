from csv import reader
from  os import  walk
import pygame.image
from settings import tile_size

def import_csv_layout(path):
    terrian_map=[]
    with open(path) as map:
        level=reader(map,delimiter= ',')
        for row in level:
            terrian_map.append(list(row))
        return terrian_map
def import_tile_image(path):
    surface=pygame.image.load(path).convert_alpha()
    x_surface= int(surface.get_width()  /tile_size)
    y_surface= int(surface.get_height()/tile_size)
    tile_image=[]
    for row in range(y_surface):
        for col in range(x_surface):
            x=col*tile_size
            y=row*tile_size
            new_surf=pygame.Surface((tile_size,tile_size),flags=pygame.SRCALPHA)
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            tile_image.append(new_surf)
    return tile_image
def import_folder(path):
    animations=[]
    for _,__,image_names in walk(path):
        for image_name in image_names:
            full_path=path+'/'+image_name
            image=pygame.image.load(full_path)
            animations.append(image)
    return animations






