
from support import *
import pygame
from settings import *
from  Tile import Tile
from  Tile import StaticTile,one_imageNoAnimated,Coin
from background import Background
from enemy import Enemy
from Player import Player
import data
from  effects import EffectExplosion

#Đại diện cho một cấp độ trò chơi và chứa các thuộc tính và phương thức khác nhau liên quan đến cấp độ đó.
class Level():
    def __init__(self,surface,current_level,create_overworld,change_health,change_coins):
        self.surface=surface #đại diện cho bề mặt mà mức được hiển thị.
        self.create_overworld=create_overworld #một chức năng hoặc phương thức được sử dụng để tạo overword của cấp độ.
        self.change_coins=change_coins #một chức năng hoặc phương pháp được sử dụng để thay đổi số lượng xu thu được trong cấp độ.
        self.word_shift=0 # sự thay đổi ngang của cấp độ.
        self.current_level=current_level #lưu số cấp hiện tại.
        self.level_data=data.levels[self.current_level] #ưu trữ dữ liệu của cấp độ hiện tại, được lấy từ từ điển data.levels
        self.new_max_level=self.level_data['unlock'] #đại diện cho cấp độ tối đa có thể được mở khóa dựa trên cấp độ hiện tại.
        self.image1=pygame.image.load('Graph/decoration/oak_woods_tileset.png') #lưu trữ hình ảnh nền hoặc trang trí của cấp độ.
        #effects
        self.explosion_sprites=pygame.sprite.GroupSingle() #có thể thêm một sprite vụ nổ duy nhất vào nhóm và dễ dàng cập nhật cũng như vẽ nó trên bề mặt trò chơi.
        #terrian set up
        terrian_layout= import_csv_layout(self.level_data['terrian']) #nhập và phân tích cú pháp tệp CSV chứa thông tin bố cục cho địa hình ở cấp độ.
        self.terrian_image = import_tile_image('Graph/decoration/oak_woods_tileset.png') #tải và trả về tệp hình ảnh có chứa các ô được sử dụng cho địa hình.
        self.terrian_sprites=self.create_tiles(terrian_layout,'terrian') # tạo và trả về một nhóm các đối tượng sprite dựa trên bố cục và mã định danh đã cho.
        #grass
        grass_layout=import_csv_layout(self.level_data['grass'])
        self.grass_sprites=self.create_tiles(grass_layout,'grass')
        #lamp
        lamp_layout = import_csv_layout(self.level_data['lamp'])
        self.lamp_sprites = self.create_tiles(lamp_layout, 'lamp')
        #rock
        rock_layout = import_csv_layout(self.level_data['rock'])
        self.rock_sprites = self.create_tiles(rock_layout, 'rock')
        #fence
        fence_layout = import_csv_layout(self.level_data['fence'])
        self.fence_sprites = self.create_tiles(fence_layout, 'fence')
        #coin
        coin_layout = import_csv_layout(self.level_data['coin'])
        self.coin_sprites = self.create_tiles(coin_layout, 'coin')
        #background
        level_width= len(terrian_layout[1])*64 #Tính toán chiều rộng của cấp độ dựa trên số cột trong bố cục địa hình nhân với chiều rộng của mỗi ô (được giả định là 64 pixel)
        self.background=Background(level_width) #quản lý và hiển thị nền của cấp độ.
        #enemy
        enemy_layout = import_csv_layout(self.level_data['enemy'])
        self.enemy_sprites = self.create_tiles(enemy_layout, 'enemy')
        #constraint
        constraint_layout = import_csv_layout(self.level_data['constraint'])
        self.constraint_sprites = self.create_tiles(constraint_layout, 'constraint')
        #player
        player_layout = import_csv_layout(self.level_data['player']) #nhập bố cục trình phát từ tệp CSV được chỉ định trong dữ liệu cấp độ. Bố cục xác định vị trí ban đầu của nhân vật người chơi trong cấp độ.
        self.player=pygame.sprite.GroupSingle() #tạo một nhóm sprite được gọi playerđể giữ nhân vật người chơi.
        self.Goal = pygame.sprite.GroupSingle() #tạo một nhóm sprite khác được gọi Goalđể giữ mục tiêu hoặc điểm cuối của cấp độ
        self.set_up_player(player_layout,change_health) # tạo và định vị trình phát sprite dựa trên bố cục, cũng như thiết lập bất kỳ chức năng bổ sung nào liên quan đến trình phát.
        #audio
        self.stomp_music=pygame.mixer.Sound('audio/action/stomp.wav')
        self.stomp_music.set_volume(0.5)
        self.coin_sound=pygame.mixer.Sound('audio/action/coin.wav')

    # cuộn cấp độ theo chiều ngang dựa trên vị trí của người chơi
    def scroll_x(self):
        player=self.player.sprite #nó lấy sprite của người chơi từ player nhóm sprite.
        player_x=player.rect.centerx # lấy tọa độ x của tâm người chơi
        direction_x=player.direction.x #truy xuất hướng x của người chơi
        if player_x<SCREEN_WIDTH/4 and direction_x<0: #người chơi ở trong phần tư bên trái của màn hình và di chuyển sang trái
            self.word_shift=16 #cuộn cấp độ sang phải.
            player.speeds=0 # đặt tốc độ của người chơi để 0ngăn chuyển động tiếp theo.
        elif player_x > SCREEN_WIDTH-SCREEN_WIDTH/4 and direction_x > 0: #người chơi ở trong phần tư bên phải của màn hình va di chuyển sang bên phải
            self.word_shift = -16 #cuộn cấp độ sang trái.
            player.speeds = 0 #đặt tốc độ của người chơi để 0ngăn chuyển động tiếp theo.
        else:
            self.word_shift = 0 #không cần cuộn ngang
            player.speeds = 15 #cho phép di chuyển bình thường.
            player.jump_speed = -26
            player.gravity = 1.7

    #tạo các loại sprite khác nhau dựa trên các giá trị bố cục, chẳng hạn như ô tĩnh, ô hoạt hình, tiền xu, kẻ thù, v.v.
    def create_tiles(self,layout,type):
        sprite_group=pygame.sprite.Group() #khởi tạo một nhóm sprite trống
        # lặp qua từng hàng và cột trong bố cục bằng các vòng lặp lồng nhau.
        for row_index,row in enumerate(layout):
            for col,val in enumerate(row):
                if val!='-1': #giá trị tại vị trí hiện tại trong bố cục không phải là '-1',
                    #tạo một sprite dựa trên loại đã chỉ định.
                    x=col*tile_size
                    y=row_index*tile_size
                    if(type=='terrian'):

                        tile_image=self.terrian_image[int(val)] #đặt biến tile_image bằng cách lập chỉ mục vào danh sách self.terrian_image bằng cách sử dụng giá trị số nguyên của val
                        sprite=StaticTile(tile_size,x,y,tile_image) #tạo các ô tĩnh cho địa hình.

                    if type=='grass':
                        if val == '0':sprite = one_imageNoAnimated(tile_size,x,y,'Graph/decoration/grass/grass_1.png')
                        if val == '4': sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/grass/grass_2 (1).png')
                        if val == '5': sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/grass/grass_3 (1).png')
                    if type=='lamp':
                        sprite = one_imageNoAnimated(tile_size,x,y,'Graph/decoration/lamp/lamp.png')
                    if type == 'rock':
                        if val == '0': sprite = one_imageNoAnimated(tile_size, x, y,
                                                                    'Graph/decoration/rock/rock_3.png')
                        if val == '1': sprite = one_imageNoAnimated(tile_size, x, y,
                                                                    'Graph/decoration/rock/rock_2.png')
                        if val == '2': sprite = one_imageNoAnimated(tile_size, x, y,
                                                                    'Graph/decoration/rock/rock_1.png')
                    if type == 'fence':
                        sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/fence/fence_1.png')
                    if type=='coin':
                        sprite =Coin(tile_size,x,y)
                    if type == 'enemy':
                        sprite = Enemy(tile_size, x, y)
                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    #chuẩn bị cho chúng để hiển thị, phát hiện va chạm và các tương tác trò chơi khác trong cấp độ.
    def set_up_player(self,layout,change_health):
        for row_index,row in enumerate(layout): #lặp lại layoutđể xác định vị trí và giá trị của các ô
            for col,val in enumerate(row):
                if val!='-1':
                    x=col*tile_size
                    y=row_index*tile_size
                    if val=='1':
                        #tạo một Player sprite với vị trí (x, y)và ththam số change_heal đã chỉ định, đồng thời thêm nó vào
                        sprite=Player((x,y),change_health)
                        self.player.add(sprite)
                    if val=='0': # đại diện cho mục tiêu hoặc điểm cuối của cấp độ.
                        sprite=one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/player/END.png') #tạo ra một nhân vật không hoạt hình
                        self.Goal.add(sprite)

    #kiểm tra sự va chạm giữa kẻ thù và các ràng buộc (chướng ngại vật) trong cấp độ.
    def enemy_collide_with_constraint(self):
        for enemy in self.enemy_sprites: # lặp lại từng sprite của kẻ thù
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False): # phát hiện các va chạm với nhóm self.constraint_sprites
                enemy.reversed() #đảo ngược hướng di chuyển của kẻ thù


    def y_movement_collide(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.terrian_sprites.sprites():
            if (sprite.rect.colliderect(player.rect) ):
                if player.direction.y > 0 and player.onCeiling==False:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True
        if player.onGround and player.direction.y > 0 or player.direction.y < 0:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False
    def x_movement_collide(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speeds

        for sprite in self.terrian_sprites.sprites():
            if (sprite.rect.colliderect(player.rect)):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right
        if player.onLeft and (player.rect.x < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.x > self.currentX or player.direction.x <= 0):
            player.onRight = False
    #interact
    def check_death(self):
        if self.player.sprite.rect.y>SCREEN_HEIGHT:
            self.create_overworld(self.current_level,0)
    def check_win(self):
        player=self.player.sprite
        goal=self.Goal.sprite
        if  player.rect.colliderect(goal.rect):
            self.create_overworld(self.current_level,self.new_max_level)

    def collide_with_enemy(self):
        sprites_collide=pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        for enemy in sprites_collide:
            enemy_center = enemy.rect.centery
            enemy_top = enemy.rect.top
            player_bottom = self.player.sprite.rect.bottom
            if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                self.player.sprite.direction.y=-15
                explosion_sprite = EffectExplosion(enemy.rect.center)
                self.explosion_sprites.add(explosion_sprite)
                self.stomp_music.play()
                enemy.kill()
            else:
                self.player.sprite.get_damed()
    def collide_with_coins(self):
        sprites_collide = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites, True)
        for coin in sprites_collide:
            self.change_coins(+1)
            self.coin_sound.play()



    def run(self):
        #draw
        self.background.draw(self.surface,self.word_shift)
        self.terrian_sprites.draw(self.surface)
        self.fence_sprites.draw(self.surface)
        self.lamp_sprites.draw(self.surface)
        self.rock_sprites.draw(self.surface)
        self.grass_sprites.draw(self.surface)
        self.enemy_sprites.draw(self.surface)
        self.coin_sprites.draw(self.surface)
        self.player.draw(self.surface)
        self.Goal.draw(self.surface)

        self.explosion_sprites.draw(self.surface)

        self.scroll_x()


        #move
        self.terrian_sprites.update(self.word_shift)
        self.grass_sprites.update(self.word_shift)
        self.lamp_sprites.update(self.word_shift)
        self.explosion_sprites.update(self.word_shift)
        self.player.update()

        self.fence_sprites.update(self.word_shift)
        self.rock_sprites.update(self.word_shift)
        self.coin_sprites.update(self.word_shift)
        self.Goal.update(self.word_shift)
        #collide with enemy
        self.collide_with_enemy()
        self.collide_with_coins()
        self.check_death()
        self.check_win()

        #enemy
        self.enemy_collide_with_constraint()
        self.enemy_sprites.update(self.word_shift)
        self.constraint_sprites.update(self.word_shift)
        self.x_movement_collide()
        self.y_movement_collide()


        pass
