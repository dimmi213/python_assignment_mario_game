import pygame
from support import import_folder
class EffectExplosion(pygame.sprite.Sprite):
    #tạo các hiệu ứng cháy nổ bằng cách quay vòng qua một chuỗi các khung hình/hình ảnh. Vụ nổ được căn giữa tại vị trí đã chỉ định ( pos) và tốc độ hoạt ảnh xác định tốc độ hiển thị khung hình.
    def __init__(self, pos):
        super().__init__()
        self.frame_index = 0 #Một số nguyên đại diện cho chỉ mục hiện tại của khung đang được hiển thị.
        self.animation_speed = 0.5 #tốc độ phát hoạt ảnh của vụ nổ.
        self.frames = import_folder('Graph/decoration/explosion') #Danh sách các hình ảnh đại diện cho các khung hình của hoạt ảnh vụ nổ.
        self.image = self.frames[self.frame_index] #Hình ảnh/khung hình hiện tại của vụ nổ.
        self.rect = self.image.get_rect(center=pos) # Một đối tượng hình chữ nhật đại diện cho vị trí và kích thước của hình ảnh vụ nổ

    #cho phép hiệu ứng vụ nổ tiến triển thông qua hoạt ảnh của nó bằng cách cập nhật khung hình/hình ảnh hiện tại. Khi hoạt ảnh hoàn tất, hình ảnh vụ nổ sẽ bị xóa khỏi trò chơi.
    def animate(self):
        self.frame_index += self.animation_speed #Thuộc tính frame_index được tăng lên bởi animation_speed. Điều này kiểm soát sự tiến triển của hình ảnh động.
        if self.frame_index >= len(self.frames): #Nếu frame_indexvượt quá hoặc bằng tổng số khung hình trong frames danh sách, điều đó có nghĩa là hoạt ảnh đã đạt hoặc vượt quá khung hình cuối cùng.
            self.kill() # loại bỏ sprite hiệu ứng nổ khỏi trò chơi. Điều này thường được thực hiện khi hoạt hình hoàn thành.
        else:
            self.image = self.frames[int(self.frame_index)] #Nếu hoạt ảnh chưa hoàn thành, hình ảnh/khung hình hiện tại của hiệu ứng vụ nổ được cập nhật dựa trên frame_index. self.frames[int(self.frame_index)] lấy hình ảnh tương ứng từ danh sách frames và nó được gán cho thuộc tính image.

    # hiệu ứng nổ được làm động và vị trí của nó được cập nhật dựa trên tham số x_shift. Phương pháp này thường được gọi một lần trên mỗi khung hình để đảm bảo hoạt ảnh và chuyển động mượt mà của hiệu ứng vụ nổ.
    def update(self, x_shift):
        self.animate() # cập nhật hoạt ảnh của hiệu ứng vụ nổ.
        self.rect.x += x_shift #Tọa độ của rectthuộc tính hiệu ứng vụ nổ được cập nhật bằng cách thêm x_shift vào nó. Điều này cho phép hiệu ứng vụ nổ di chuyển theo chiều ngang bằng cách dịch chuyển vị trí của nó.
