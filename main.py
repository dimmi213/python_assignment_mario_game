import sys

import pygame
from  Level import Level
from settings import  *
import colorss
from overworld import Overworld
from UI import UI
from pygame.image import load
from menu import Menu
from Tile import *
from Player import *
from check import Check

import data
class Game:
    def __init__(self):
        self.max_level=0
        self.max_health = 3
        self.current_health = 3
        self.coins = 0
        self.overworld = Overworld(0,self.max_level,SCREEN,self.create_level)
        self.status='overworld'
        self.ui=UI(SCREEN)
        # self.mainOverSound=pygame.mixer.Sound('audio/Pokemon Black & White OST - 5-198 The First Day.mp3')
        # self.mainlevelSound = pygame.mixer.Sound('audio/Pokemon Black & White OST - 6-198 Kanoko Town.mp3')
        # self.mainlevelSound.set_volume(0.5)
        # self.mainOverSound.set_volume(0.5)
        # self.mainOverSound.play(loops=-1)

    def create_level(self,current_level):
        self.level= Level( SCREEN,current_level,self.create_overworld,self.change_health,self.change_coins)
        self.status='level'
        # self.mainOverSound.stop()
        # self.mainlevelSound.play(loops=-1)
    def create_overworld(self, current_level,max_level):
        if max_level>self.max_level:
            self.max_level=max_level
        self.overworld = Overworld(current_level,self.max_level,SCREEN,self.create_level)
        self.status='overworld'
        # self.mainlevelSound.stop()
        # self.mainOverSound.play(loops=-1)
    def change_coins(self,num):
        self.coins+=num
    def change_health(self,num):
        self.current_health+=num

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 3
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, SCREEN, self.create_level)
            self.status = 'overworld'
            # self.mainlevelSound.stop()
            # self.mainOverSound.play(loops=-1)




    def run(self):
        print(self.status)
        if self.status=='overworld':
            self.overworld.run()
        else :
            self.level.run()
            self.ui.show_coins(self.coins)
            self.ui.show_health(self.current_health)
            self.check_game_over()



SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game=Game()
menu = Menu(SCREEN)

#khởi tạo con chuột
surf = load('./Graph/cursor/mouse.png').convert_alpha()
cursor = pygame.cursors.Cursor((0,0), surf)
pygame.mouse.set_cursor(cursor)

# Gọi hàm vẽ menu
menu.create_menu()

# Tạo background và level
background_image = pygame.image.load('./Graph/decoration/background/background.png').convert_alpha()
# level = Level(map, SCREEN)
# level= Level( SCREEN,0,create_overworld,change_health,change_coins)
check = Check(map,SCREEN)
CLOCK= pygame.time.Clock()

def offMusicbggame():
    if menu.onMusicBgGame == True:
        pygame.mixer.music.play(-1)
    elif menu.onMusicBgGame == False:
        pygame.mixer.music.stop()



# Tạo biến boolean để kiểm tra trạng thái tạm dừng của trò chơi
paused = False
offMusicbggame()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Nếu trạng thái là đang chạy, đặt thành tạm dừng và hiển thị menu tạm dừng
                if not paused:
                    paused = True
                    menu_choice = menu.pause_menu(SCREEN)
                    if menu_choice == "resume":
                        menu_choice = ""
                        paused = False
                    elif menu_choice == "quit":
                        menu_choice = ""
                        pygame.quit()
                        sys.exit()
                    elif menu_choice == "replay":
                        menu_choice=""
                        # level = Level(map, SCREEN)  # truyền vào map_data và main_screen khi khởi tạo Level
                        paused = False
                        # Chạy trò chơi từ đầu
                        SCREEN.fill('black')
                        SCREEN.blit(background_image, (0, 0))
                        game.run()

                        # level.run()
                        pygame.display.update()
                        CLOCK.tick(60)
                # Nếu trạng thái là đang tạm dừng, đặt lại thành đang chạy
                else:
                    paused = False

    # Nếu trạng thái là đang chạy, tiếp tục chơi
    if not paused:
        SCREEN.fill('black')
        SCREEN.blit(background_image, (0, 0))
        game.run()
        # level.run()
        pygame.display.update()
        CLOCK.tick(60)

# kiểm tra gameover từ out_of_map() hoặc là out_health
        if check.check_gameover():
            menu.gameover_menu(SCREEN)
            menu_choice_gameover = menu.gameover_menu(SCREEN)
            if menu_choice_gameover == 'quit':
                pygame.quit()
                sys.exit()
            elif menu_choice_gameover == 'replay':
                # level = Level(map, SCREEN)  # truyền vào map_data và main_screen khi khởi tạo Level
                paused = False
                # Chạy trò chơi từ đầu
                SCREEN.fill('black')
                SCREEN.blit(background_image, (0, 0))
                game.run()

                # level.run()
                pygame.display.update()
                CLOCK.tick(60)
        if check.check_win():
            menu.win_menu(SCREEN)
            menu_choice_win = menu.win_menu(SCREEN)
            if menu_choice_win == 'quit':
                pygame.quit()
                sys.exit()
            elif menu_choice_win == 'replay':
                # level = Level(map, SCREEN)  # truyền vào map_data và main_screen khi khởi tạo Level
                paused = False
                # Chạy trò chơi từ đầu
                SCREEN.fill('black')
                SCREEN.blit(background_image, (0, 0))
                game.run()
                # level.run()
                pygame.display.update()
                CLOCK.tick(60)

# def main():
#     while True:
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         SCREEN.fill(colorss.black)
#         game.run()
#         # map.run()
#         pygame.display.update()
#         CLOCK.tick(60)




# Press the green button in the gutter to run the script.

# main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
