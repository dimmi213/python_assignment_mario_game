from Tile import AnimatedImage
from  random import randint
import  pygame

#Lớp Enemy kế thừa các phương thức và thuộc tính từ lớp AnimatedImage, cho phép nó hiển thị và làm động hình ảnh kẻ thù.
class Enemy(AnimatedImage):
    def __init__(self, size, x, y, ):
        # size: Kích thước của hình ảnh kẻ thù.
        # x,y: tọa độ của kẻ thù
        super().__init__(size, x, y, 'Graph/decoration/enemy' ) #gọi hàm tạo của lớp cha AnimatedImage, chuyển các tham số size, xvà ycùng với đường dẫn đến tệp hình ảnh của kẻ thù.
        self.rect.y+=size-self.image.get_size()[1] # điều chỉnh để định vị kẻ thù ở độ cao phù hợp trên màn hình.
        self.speed=randint(2,4) #đặt thành một số nguyên ngẫu nhiên trong khoảng từ 2 đến 4, xác định tốc độ di chuyển của kẻ thù

    #cập nhật vị trí của đối tượng địch
    def move(self):
        #di chuyển kẻ thù theo chiều ngang dựa trên thuộc tính speed của nó
        self.rect.x+=self.speed #Khoảng cách di chuyển thực tế sẽ phụ thuộc vào tần số mà phương thức này được gọi và giá trị của speed.

    # đảo ngược hướng di chuyển của kẻ thù
    def move_reverse(self):
        if self.speed<0: #nếu chuyển động sang trái
            self.image=pygame.transform.flip(self.image,True,False) # lật hình ảnh của kẻ thù theo chiều ngang

    # đảo ngược hướng di chuyển của kẻ thù.
    def reversed(self):
        self.speed*=-1 #nhân thuộc tính speed của kẻ thù với -1. Âm thành dương, dương thành âm


    #phương pháp này update()kết hợp một số khía cạnh trong hành vi của kẻ thù, bao gồm chuyển động, hoạt ảnh và đảo ngược hướng, để cập nhật trạng thái của kẻ thù trong mỗi khung hình của vòng lặp trò chơi.
    def update(self,shift): #tham số shift, đại diện cho mức độ dịch chuyển vị trí của kẻ thù theo chiều ngang.
        self.rect.x += shift #di chuyển kẻ thù theo chiều ngang theo sự thay đổi được chỉ định
        self.frames_moving() #để cập nhật các khung hoạt hình của kẻ thù.
        self.move() #cập nhật vị trí của kẻ thù dựa trên tốc độ hiện tại của nó. Điều này di chuyển kẻ thù theo hướng hiện tại của nó.
        self.move_reverse() # kiểm tra xem tốc độ của kẻ thù có nên đảo ngược dựa trên hướng hiện tại của nó hay không.