import random
import sys
import pygame
from button import Button
from settings import *
from Tile import *

pygame.init()

class Menu:
    def __init__(self, screen):
        self.screen = screen #Tham chiếu đến màn hình hiển thị menu.
        self.onMusic = True #Một boolean cho biết nhạc được bật hay tắt.
        self.onOrOff = 3 # Giá trị biểu thị trạng thái
        self.onOrOffBgGame = 3 #Một giá trị cho biết trạng thái của thứ gì đó liên quan đến trò chơi nền, cũng có giá trị là 3.
        self.onMusicBgGame = True #Một giá trị boolean cho biết nhạc nền trò chơi được bật hay tắt.
        pygame.mixer.music.load('audio/Pokemon Black & White OST - 6-198 Kanoko Town.mp3')
        pygame.mixer.music.set_volume(1)


    def create_menu(self):
        # pygame.mixer.music.play(-1)
        self.offMusic() #offMusic()phương thức có khả năng tắt nhạc menu hoặc đặt cài đặt nhạc thích hợp.
        # background_menu = pygame.image.load("graphics/background/background_menu_2.png")
        background_menu = pygame.image.load("./Graph/decoration/background/background_bg.png")
        pygame.display.set_caption("Menu") #đặt chú thích của cửa sổ trò chơi thành "Menu"

        while True:

            # thiết lập và vẽ màn hình menu với hình nền, văn bản menu và các nút để phát, tùy chọn và tùy chọn thoát.
            self.screen.blit(background_menu, (0, 0)) #Hình ảnh background_menu được chiếu lên màn hình tại tọa độ (0, 0)
            MENU_MOUSE_POS = pygame.mouse.get_pos() # lấy vị trí chuột
            MENU_TEXT = self.get_font(34).render("MARIO GAME", True, "#b68f40") #ăn bản được hiển thị với thông báo "CUỘC PHIÊU LƯU ĐÊM GIÁNG SINH CỦA SANTA", sử dụng giá trị màu là "#b68f40"
            MENU_RECT = MENU_TEXT.get_rect(center=(620, 120)) #Hình chữ nhật bao quanh của văn bản menu, tâm của nó được đặt thành tọa độ (620, 120)
            PLAY_BUTTON = Button(image=pygame.image.load("./Graph/menu/Play Rectq.png"), pos=(620, 350),
                                 text_input="PLAY", font=self.get_font(25), base_color="#1F697D", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("./Graph/menu/Options Rectq.png"), pos=(620, 450),
                                    text_input="OPTIONS", font=self.get_font(25), base_color="#1F697D",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("./Graph/menu/Quit Rectq.png"), pos=(620, 550),
                                 text_input="QUIT", font=self.get_font(25), base_color="#1F697D", hovering_color="White")

            #xử lý việc hiển thị và cập nhật văn bản menu và các nút trên màn hình dựa trên vị trí chuột.
            self.screen.blit(MENU_TEXT, MENU_RECT) # hiển thị MENU_TEXT lên màn hình, Văn bản được làm mờ ở vị trí được chỉ định bởi MENU_RECT, đại diện cho vị trí trung tâm của văn bản.
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]: #Một vòng lặp được sử dụng để lặp qua danh sách các nút [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON].
                button.changeColor(MENU_MOUSE_POS) # phương thức changeColor() được gọi trên đối tượng nút, chuyển đối số MENU_MOUSE_POSdưới dạng đối số. Phương pháp này có khả năng thay đổi màu của nút dựa trên vị trí của chuột.
                button.update(self.screen)  #cập nhật giao diện và vị trí của nút trên màn hình.

            #xử lý các tương tác của người dùng với màn hình menu, chẳng hạn như nhấp vào nút phát, tùy chọn hoặc thoát và thực hiện các hành động thích hợp dựa trên đầu vào của người dùng.
            for event in pygame.event.get(): #Vòng lặp lặp lại qua từng sự kiện trong pygame.event.get().
                if event.type == pygame.QUIT: #Nếu loại sự kiện là pygame.QUIT, điều đó có nghĩa là người dùng đã nhấp vào nút đóng cửa sổ.
                    pygame.quit() #thoát khỏi mô-đun pygame
                    sys.exit() #  thoát khỏi chương trình Python.
                if event.type == pygame.MOUSEBUTTONDOWN: #người dùng đã nhấp vào nút chuột.
                    #checkForInput()được gọi trên mỗi đối tượng nút để kiểm tra xem nhấp chuột có xảy ra trong ranh giới của nút đó hay không. The MENU_MOUSE_POSđược truyền dưới dạng đối số để lấy vị trí chuột hiện tại.
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS): #Nếu nhấp chuột xảy ra trong ranh giới của nút phát
                        return #Điều này có thể chỉ ra rằng người dùng muốn tiếp tục chơi trò chơi.
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS): #Nếu nhấp chuột xảy ra trong ranh giới của nút tùy chọn
                        self.show_options_screen(self.onOrOff, self.onOrOffBgGame) #chuyển cài đặt bật/tắt hiện tại cho nhạc và trò chơi nền.

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS): #Nếu nhấp chuột xảy ra trong ranh giới của nút thoát
                        pygame.quit() #hàm được gọi để thoát khỏi mô-đun pygame
                        sys.exit() #được gọi để thoát khỏi chương trình Python.

            pygame.display.update() #để cập nhật nội dung của toàn bộ bề mặt hiển thị



    def pause_menu(self, screen):

        RESUME_BUTTON = Button(image=pygame.image.load("./Graph/menu/Play Rectq.png"), pos=(620, 250),
                             text_input="RESUME", font=self.get_font(25), base_color="#008DB9", hovering_color="WHITE")

        # REPLAY_BUTTON = Button(image=pygame.image.load("./Graph/menu/Options Rectq.png"), pos=(620, 350),
        #                         text_input="REPLAY", font=self.get_font(25), base_color="#008DB9",
        #                         hovering_color="WHITE")
        QUIT_BUTTON = Button(image=pygame.image.load("./Graph/menu/Quit Rectq.png"), pos=(620, 350),
                             text_input="QUIT", font=self.get_font(25), base_color="#008DB9", hovering_color="WHITE")

        # Hiển thị menu
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Kiểm tra xem người dùng có nhấp chuột không
            if pygame.mouse.get_pressed()[0]:
                # Kiểm tra xem vị trí chuột có nằm trong resume_rect không
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Tiếp tục chơi
                    return "resume"

                # Kiểm tra xem vị trí chuột có nằm trong replay_rect không
                # elif REPLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     # Chơi lại từ đầu
                #     return "replay"
                # Kiểm tra xem vị trí chuột có nằm trong quit_rect không
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Thoát trò chơi
                    return "quit"

            for button in [RESUME_BUTTON , QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            pygame.display.update()

    def gameover_menu(self, screen):

        # Hiển thị Game Over và nút Replay
        font_menu = pygame.font.Font("./fonts/Press_Start_2P/PressStart2P-Regular.ttf", 70)
        gameover_text = font_menu.render("Game Over", True, (168, 21, 11))
        gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))

        REPLAY_BUTTON = Button(image=pygame.image.load("./Graph/menu/Options Rectq.png"), pos=(620, 450),
                               text_input="REPLAY", font=self.get_font(25), base_color="#008DB9",
                               hovering_color="WHITE")
        QUIT_BUTTON = Button(image=pygame.image.load("./Graph/menu/Quit Rectq.png"), pos=(620, 550),
                             text_input="QUIT", font=self.get_font(25), base_color="#008DB9", hovering_color="WHITE")

        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Lấy vị trí chuột
            mouse_pos = pygame.mouse.get_pos()

            # Kiểm tra xem người dùng có nhấp chuột không
            if pygame.mouse.get_pressed()[0]:
                # Kiểm tra xem vị trí chuột có nằm trong replay_rect không
                if REPLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                # Chơi lại từ đầu
                    return "replay"
                # Kiểm tra xem vị trí chuột có nằm trong quit_rect không
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Thoát trò chơi
                    return "quit"
            screen.blit(gameover_text, gameover_rect)

            for button in [REPLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            pygame.display.update()

    def win_menu(self, screen):

        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            font_menu = pygame.font.Font("./fonts/Press_Start_2P/PressStart2P-Regular.ttf", 60)
            win_text = font_menu.render("Congratulations!", True, (168, 21, 11))
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))

            REPLAY_BUTTON = Button(image=pygame.image.load("./Graph/menu/Options Rectq.png"), pos=(620, 450),
                                   text_input="REPLAY", font=self.get_font(25), base_color="#008DB9",
                                   hovering_color="WHITE")
            QUIT_BUTTON = Button(image=pygame.image.load("./Graph/menu/Quit Rectq.png"), pos=(620, 550),
                                 text_input="QUIT", font=self.get_font(25), base_color="#008DB9",
                                 hovering_color="WHITE")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if pygame.mouse.get_pressed()[0]:
                # Kiểm tra xem vị trí chuột có nằm trong replay_rect không
                if REPLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                # Chơi lại từ đầu
                    return "replay"
                # Kiểm tra xem vị trí chuột có nằm trong quit_rect không
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Thoát trò chơi
                    return "quit"

            screen.blit(win_text, win_rect)

            for button in [REPLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            pygame.display.update()

    def show_options_screen(self, onOrOff, onOrOffBgGame):

        # Load background image and set window caption
        options_bg = pygame.image.load("./Graph/decoration/background/background_menu_2.png")
        pygame.display.set_caption("Options")

        # Create button to return to main menu
        BACK_BUTTON = Button(image=pygame.image.load("./Graph/menu/Play Rectq.png"), pos=(125, 100),
                             text_input="BACK", font=self.get_font(25), base_color="#1F697D", hovering_color="White")

        # Loop to display options screen
        while True:
            self.screen.blit(options_bg, (0, 0))
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            # Check for button interactions

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ONMUSIC_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.onOrOff = self.onOrOff + 1
                        if onOrOff % 2 == 0:
                            self.onMusic = True

                            self.create_menu()
                            return
                        else:
                            self.onMusic = False

                            self.create_menu()
                            return
                    # elif ONMUSIC_BG_GAME_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    #     self.onOrOffBgGame = self.onOrOffBgGame + 1
                    #     if self.onOrOffBgGame % 2 == 0:
                    #         self.onMusicBgGame = True
                    #         self.create_menu()
                    #         return
                    #     else:
                    #         self.onMusicBgGame = False
                    #         self.create_menu()
                    #         return
                    elif BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        return

            if onOrOff % 2 != 0:
                text_input = "OFF MUSIC MENU"
            else:
                text_input = "ON MUSIC MENU"

            # if onOrOffBgGame % 2 != 0:
            #     text_inputBGGame = "OFF MUSIC GAME"
            # else:
            #     text_inputBGGame = "ON MUSIC GAME"

            ONMUSIC_BUTTON = Button(image=pygame.image.load("./Graph/menu/Options Rectq.png"), pos=(620, 450),
                                    text_input=text_input, font=self.get_font(25), base_color="#008DB9",
                                    hovering_color="WHITE")

            # ONMUSIC_BG_GAME_BUTTON = Button(image=pygame.image.load("./Graph/menu/Options Rectq.png"), pos=(620, 550),
            #                                 text_input=text_inputBGGame, font=self.get_font(25), base_color="#008DB9",
            #                                 hovering_color="WHITE")

            for button in [BACK_BUTTON, ONMUSIC_BUTTON]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(self.screen)

            pygame.display.update()



    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("./fonts/Press_Start_2P/PressStart2P-Regular.ttf", size)

    def offMusic(self):
        if self.onMusic == False:
            pygame.mixer.music.stop()
            print('cac')
        elif self.onMusic == True:
            pygame.mixer.music.play(-1)

    # def checkOffMusicBgGame(self):
    #     if self.onMusicBgGame == False:
    #         return False
    #         # pygame.mixer.music.stop()
    #     elif self.onMusicBgGame == True:
    #         return True
    #         # pygame.mixer.music.play(-1)


