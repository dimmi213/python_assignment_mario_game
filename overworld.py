import pygame

from background import Background
from data import levels
import colorss
from support import *

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,speed,path):
        super().__init__()

        self.speedq=speed
        self.image=pygame.image.load(path)
        if status=='availible':
            self.status=status
        else:
            self.status='locked'
        self.rect=self.image.get_rect(center=pos)
        self.Detective_zone=pygame.Rect(self.rect.centerx-self.speedq/2,self.rect.centery-self.speedq/2,self.speedq,self.speedq)
    def update(self):
        if self.status!='availible':
            change_image=self.image.copy()
            change_image.fill(colorss.black,None,pygame.BLEND_RGBA_MULT)
            self.image.blit(change_image,(0,0))
class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        self.frame=import_folder('Graph/decoration/character/idle')
        super().__init__()
        self.pos=pos
        self.index=0
        self.image=self.frame[int(self.index)]
        self.rect = self.image.get_rect(center=pos)
    def animation(self):
        self.index+=0.15
        if self.index >= len(self.frame):
            self.index = 0
        self.image = self.frame[int(self.index)]
    def update(self):
        self.animation()
        self.rect.center=self.pos
class Overworld:

    def __init__(self,start_level,max_level,surface,create_level):
        self.create_level = create_level
        self.current_level = start_level
        self.max_level = max_level
        self.display_surface = surface
        self.moving_direction = pygame.math.Vector2(0, 0)
        self.moving = False
        self.speed = 8
        self.node_setup()
        self.Icon_setup()
        self.background=Background(64*11)


    def node_setup(self):
        self.node_sprites =pygame.sprite.Group()
        for index,node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite=Node(node_data['node_pos'],'availible',self.speed,node_data['node_graph'])
            else :
                node_sprite=Node(node_data['node_pos'],'not availible',self.speed,node_data['node_graph'])
            self.node_sprites.add(node_sprite)

    def lines_draw(self):
        points=[Nodedata['node_pos'] for index,Nodedata in enumerate(levels.values()) if index<=self.max_level ]
        if(len(points)!=1):
            pygame.draw.lines(self.display_surface,colorss.red,False,points,6)
    def Icon_setup(self):
        self.Icon=pygame.sprite.GroupSingle()
        sprite=Icon(self.node_sprites.sprites()[self.current_level].rect.center)
        self.Icon.add(sprite)
    def input(self):
        keys=pygame.key.get_pressed() #nhận tat cả các phím hiện đang được nhấn
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level<self.max_level: # kiểm tra xem người dùng có đang nhấn mũi tên phải và mức hiện tại có đang thấp hơn mức tối đa hay không
                self.moving_direction=self.moving_setup('next') # đặt hứớng di chuyển thành tiếp theo
                self.current_level+=1 #tăng mức hiện tại lên 1
                self.moving=True # đặt cờ di chuyển thành True
            if keys[pygame.K_LEFT] and self.current_level>0: # Kiểm tra xem người dùng đã nhấn mũi tên trái và mức hiện tại có lớn hơn 0
                self.moving_direction = self.moving_setup('previous') #đặt hướng di chuyển thành trước
                self.current_level+=-1 #giảm mức hiện tại xuống 1
                self.moving = True # đặt cờ di chuyển thành True
            if keys[pygame.K_RETURN]: # nếu nhấn phím 0
                self.create_level(self.current_level) # gọi phương thc create_level(mức hiện tại làm đối số)
    def moving_setup(self,status):
        if status=='next': #xác định xem có chuyển qua cấp độ tiếp theo
            start = pygame.math.Vector2(self.node_sprites.sprites()[self.current_level].rect.center) #đặt start thành tâm của nút sprite cấp hiện tại
            end=pygame.math.Vector2(self.node_sprites.sprites()[self.current_level+1].rect.center) # end thành tâm của nút sprite cấp tiếp theo
        #pygame.math.Vector2() là một lớp trong Pygame đại diện cho một vectơ 2D có thành phần x và y. tính toán hướng di chuyển cho nhân vật người chơi khi di chuyển từ nút này sang nút khác trên bản đồ.
        else: #hay cấp độ trước đó
            start = pygame.math.Vector2(self.node_sprites.sprites()[self.current_level].rect.center) # đặt start thành trunh tâm của nút sprite cấp hiện tại
            end = pygame.math.Vector2(self.node_sprites.sprites()[self.current_level - 1].rect.center) #end thành trung tâm của nút sprite cấp trước đó
        return (end-start).normalize() #tính toán và trả về vector chuẩn hóa giữa start và end (lấy vector chỉ hướng chuẩn hóa từ start đến end)

    def update_icon_pos(self): #cập nhật vị trí biểu tuợng của người chơi
        if self.moving and self.moving_direction: #nếu người chơi đang di chuyển và có hướng chuyển động (moving=True, moving_direction!=0)
            self.Icon.sprite.pos+=self.moving_direction*self.speed #vị trí biểu tượng được cập nhật bằng cách cộng thêm vecto chuyển động chuẩn hóa x tốc độ của trình phát hiện tại của biểu tượng
            target_node=self.node_sprites.sprites()[self.current_level] #truy cập nút sprite hiện tại trong danh sách các nút sprite
            if target_node.Detective_zone.collidepoint(self.Icon.sprite.pos): #nếu biểu tượng của người chơi đã đến vùng thám hiểm của nút mục tiêu
                self.moving=False #chuyển động dừng lại
                self.moving_direction=pygame.math.Vector2(0,0) #hướng di chuyển đặt thành vector 0
    def run(self):
        self.background.draw(self.display_surface,0)
        self.input()
        self.update_icon_pos()
        self.Icon.update()
        self.node_sprites.update()
        self.lines_draw()
        self.node_sprites.draw(self.display_surface)

        self.Icon.draw(self.display_surface)

