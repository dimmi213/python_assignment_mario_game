import pygame
from menu import Menu
from support import *
from settings import *
from  Tile import Tile
from  Tile import StaticTile,one_imageNoAnimated,Coin
from background import Background
from enemy import Enemy
from Player import Player
import data
from  effects import EffectExplosion

class Check():
    def __init__(self, map_data, surface):
        self.surface = surface
        # self.map = self.setup_map(map_data)
        self.scroll_speed = 0  # tốc độ di chuyển của màn hình khi đi hết map
        # nhạc game
        self.game_play_sound = pygame.mixer.Sound('audio/gameplaysound.mp3')
        self.game_play_sound.set_volume(0.25)  # âm lượng 1 nửa

        self.menu = Menu(surface)
        self.checkwin = False
        self.current_level = 0
        self.level_data = data.levels[self.current_level]

        self.current_health = 6

        # self.level_data = data.levels[self.current_level]
        player_layout = import_csv_layout(self.level_data['player'])  # nhập bố cục trình phát từ tệp CSV được chỉ định trong dữ liệu cấp độ. Bố cục xác định vị trí ban đầu của nhân vật người chơi trong cấp độ.
        self.player = pygame.sprite.GroupSingle()  # tạo một nhóm sprite được gọi playerđể giữ nhân vật người chơi.
        self.Goal = pygame.sprite.GroupSingle()  # tạo một nhóm sprite khác được gọi Goalđể giữ mục tiêu hoặc điểm cuối của cấp độ
        self.set_up_player(player_layout, self.change_health)
        #self.player = Player()
        self.set_up_player(player_layout,self.change_health)

    def change_health(self,num):
        self.current_health+=num

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

    def out_of_map(self):  # rớt xuống overworld
        player = self.player.sprite
        if player.rect.centery > 1000:
            return 1

    # def out_of_heart(self):
    #     heart = self.player.sprite.heart
    #     if heart.total <= 0:
    #         return 1

    def change_health(self,num):
        self.current_health+=num

    def out_of_heart(self):
        # heart = self.player.sprite.heart
        if self.current_health <= 0:
            return 1

    def check_gameover(self):
       if self.out_of_map() == 1:
           return True
       if self.out_of_heart() == 1:
           return True

    def check_win(self):
        if self.checkwin == True:
            return True

    # def setup_map(self, map_data):
    #     # effects
    #     self.explosion_sprites = pygame.sprite.GroupSingle()  # có thể thêm một sprite vụ nổ duy nhất vào nhóm và dễ dàng cập nhật cũng như vẽ nó trên bề mặt trò chơi.
    #     # terrian set up
    #     terrian_layout = import_csv_layout(self.level_data[
    #                                            'terrian'])  # nhập và phân tích cú pháp tệp CSV chứa thông tin bố cục cho địa hình ở cấp độ.
    #     self.terrian_image = import_tile_image(
    #         'Graph/decoration/oak_woods_tileset.png')  # tải và trả về tệp hình ảnh có chứa các ô được sử dụng cho địa hình.
    #     self.terrian_sprites = self.create_tiles(terrian_layout,
    #                                              'terrian')  # tạo và trả về một nhóm các đối tượng sprite dựa trên bố cục và mã định danh đã cho.
    #     # grass
    #     grass_layout = import_csv_layout(self.level_data['grass'])
    #     self.grass_sprites = self.create_tiles(grass_layout, 'grass')
    #     # lamp
    #     lamp_layout = import_csv_layout(self.level_data['lamp'])
    #     self.lamp_sprites = self.create_tiles(lamp_layout, 'lamp')
    #     # rock
    #     rock_layout = import_csv_layout(self.level_data['rock'])
    #     self.rock_sprites = self.create_tiles(rock_layout, 'rock')
    #     # fence
    #     fence_layout = import_csv_layout(self.level_data['fence'])
    #     self.fence_sprites = self.create_tiles(fence_layout, 'fence')
    #     # coin
    #     coin_layout = import_csv_layout(self.level_data['coin'])
    #     self.coin_sprites = self.create_tiles(coin_layout, 'coin')
    #     # background
    #     level_width = len(terrian_layout[
    #                           1]) * 64  # Tính toán chiều rộng của cấp độ dựa trên số cột trong bố cục địa hình nhân với chiều rộng của mỗi ô (được giả định là 64 pixel)
    #     self.background = Background(level_width)  # quản lý và hiển thị nền của cấp độ.
    #     # enemy
    #     enemy_layout = import_csv_layout(self.level_data['enemy'])
    #     self.enemy_sprites = self.create_tiles(enemy_layout, 'enemy')
    #     # constraint
    #     constraint_layout = import_csv_layout(self.level_data['constraint'])
    #     self.constraint_sprites = self.create_tiles(constraint_layout, 'constraint')
    #     # player
    #     player_layout = import_csv_layout(self.level_data[
    #                                           'player'])  # nhập bố cục trình phát từ tệp CSV được chỉ định trong dữ liệu cấp độ. Bố cục xác định vị trí ban đầu của nhân vật người chơi trong cấp độ.
    #     self.player = pygame.sprite.GroupSingle()  # tạo một nhóm sprite được gọi playerđể giữ nhân vật người chơi.
    #     self.Goal = pygame.sprite.GroupSingle()  # tạo một nhóm sprite khác được gọi Goalđể giữ mục tiêu hoặc điểm cuối của cấp độ
    #     #self.set_up_player(player_layout,change_health)  # tạo và định vị trình phát sprite dựa trên bố cục, cũng như thiết lập bất kỳ chức năng bổ sung nào liên quan đến trình phát.
    #     # audio
    #     self.stomp_music = pygame.mixer.Sound('audio/action/stomp.wav')
    #     self.stomp_music.set_volume(0.5)
    #     self.coin_sound = pygame.mixer.Sound('audio/action/coin.wav')
    #
    # # tạo các loại sprite khác nhau dựa trên các giá trị bố cục, chẳng hạn như ô tĩnh, ô hoạt hình, tiền xu, kẻ thù, v.v.
    # def create_tiles(self, layout, type):
    #     sprite_group = pygame.sprite.Group()  # khởi tạo một nhóm sprite trống
    #     # lặp qua từng hàng và cột trong bố cục bằng các vòng lặp lồng nhau.
    #     for row_index, row in enumerate(layout):
    #         for col, val in enumerate(row):
    #             if val != '-1':  # giá trị tại vị trí hiện tại trong bố cục không phải là '-1',
    #                 # tạo một sprite dựa trên loại đã chỉ định.
    #                 x = col * tile_size
    #                 y = row_index * tile_size
    #                 if (type == 'terrian'):
    #                     tile_image = self.terrian_image[
    #                         int(val)]  # đặt biến tile_image bằng cách lập chỉ mục vào danh sách self.terrian_image bằng cách sử dụng giá trị số nguyên của val
    #                     sprite = StaticTile(tile_size, x, y, tile_image)  # tạo các ô tĩnh cho địa hình.
    #
    #                 if type == 'grass':
    #                     if val == '0': sprite = one_imageNoAnimated(tile_size, x, y,
    #                                                                 'Graph/decoration/grass/grass_1.png')
    #                     if val == '4': sprite = one_imageNoAnimated(tile_size, x, y,
    #                                                                 'Graph/decoration/grass/grass_2 (1).png')
    #                     if val == '5': sprite = one_imageNoAnimated(tile_size, x, y,
    #                                                                 'Graph/decoration/grass/grass_3 (1).png')
    #                 if type == 'lamp':
    #                     sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/lamp/lamp.png')
    #                 if type == 'rock':
    #                     if val == '0': sprite = one_imageNoAnimated(tile_size, x, y,
    #                                                                 'Graph/decoration/rock/rock_3.png')
    #                     if val == '1': sprite = one_imageNoAnimated(tile_size, x, y,
    #                                                                 'Graph/decoration/rock/rock_2.png')
    #                     if val == '2': sprite = one_imageNoAnimated(tile_size, x, y,
    #                                                                 'Graph/decoration/rock/rock_1.png')
    #                 if type == 'fence':
    #                     sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/fence/fence_1.png')
    #                 if type == 'coin':
    #                     sprite = Coin(tile_size, x, y)
    #                 if type == 'enemy':
    #                     sprite = Enemy(tile_size, x, y)
    #                 if type == 'constraint':
    #                     sprite = Tile(tile_size, x, y)
    #
    #                 sprite_group.add(sprite)
    #     return sprite_group