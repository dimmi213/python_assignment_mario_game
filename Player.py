import  pygame
from colorss import *
import support
from settings import *
from math import sin

#cập nhật trạng thái của người chơi, xử lý chuyển động và va chạm, đồng thời tạo hoạt ảnh cho nhân vật người chơi.
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,change_health):
        super().__init__()
        self.change_health=change_health #Tham chiếu đến một chức năng có thể được sử dụng để thay đổi sức khỏe của người chơi.
        self.setup_animations() #Một từ điển chứa các khung hình động cho các trạng thái khác nhau của người chơi (ví dụ: không hoạt động, đang chạy, nhảy).
        self.frame_index=0 #Một chỉ số đại diện cho khung hoạt hình hiện tại.
        self.animation_speed=0.15 #Tốc độ quay vòng của các khung hình động.\
        #Các thuộc tính liên quan đến chuyển động:
        self.status='idle' #Trạng thái hiện tại của trình phát (ví dụ: idle, running, jumping).
        self.facing_right=True #Một boolean cho biết người chơi đang quay mặt sang phải hay trái.
        self.onGround=True # Một giá trị boolean cho biết người chơi có ở trên mặt đất hay không.
        self.onCeiling=False #Một giá trị boolean cho biết người chơi có ở trên trần nhà hay không.
        self.onLeft=False #Một giá trị boolean cho biết liệu người chơi có đang dựa vào bức tường ở phía bên trái hay không.
        self.onRight=False #Một giá trị boolean cho biết liệu người chơi có đang dựa vào bức tường ở phía bên phải hay không.
        #Các thuộc tính khác:
        self.image=self.animations['idle'][self.frame_index] #Hình ảnh hiện tại của sprite người chơi.
        self.rect = self.image.get_rect(topleft=pos) #Hộp giới hạn hình chữ nhật của nhân vật người chơi.
        self.invincible=False #Một giá trị boolean cho biết liệu người chơi hiện có bất khả chiến bại hay không.
        self.invincible_duration=800 #Khoảng thời gian bất khả chiến bại của người chơi sau khi bị thương.
        self.hurt_time=0 #Thời điểm người chơi bị đau lần cuối.
        #Thuộc tính liên quan đến âm thanh:
        self.hit_sound=pygame.mixer.Sound('audio/action/hit.wav') #Hiệu ứng âm thanh phát ra khi người chơi bị đánh
        self.jump_sound=pygame.mixer.Sound('audio/action/jump.wav') #Hiệu ứng âm thanh phát ra khi người chơi nhảy.
        self.jump_sound.set_volume(0.2)
        #chuyen dong nhan vat

        self.direction = pygame.math.Vector2(0, 0)
        self.jump_speed=-16
        self.gravity= 0.8
        self.speed= 8
    def setup_animations(self): # thiết lập các khung hình động cho các trạng thái trình phát khác nhau.
        character_path = 'Graph/decoration/character/'
        self.animations={'idle':[],'fall':[],'jump':[]} #khởi tạo dưới dạng từ điển với các khóa đại diện cho các trạng thái người chơi khác nhau (ví dụ: idle, running, jumping) và danh sách trống làm giá trị tương ứng.
        for animation in self.animations.keys() :
            full_path=character_path+animation #nối character_pathvà animationđể tạo đường dẫn đầy đủ đến thư mục hoạt ảnh.
            self.animations[animation]=support.import_folder(full_path) #nhập các khung hình từ thư mục đã chỉ định và gán chúng cho khóa hoạt hình tương ứng trong từ điển self.animations

    #xác định khung hoạt ảnh nào sẽ được sử dụng để hiển thị nhân vật trình phát.
    #xác định trạng thái của người chơi dựa trên hướng thẳng đứng của họ ( self.direction.y)
    def setup_status(self):
        if self.direction.y<0: #gười chơi đang di chuyển lên trên, biểu thị một bước nhảy
            self.status='jump' # trạng thái được đặt thành 'jump'.
        elif self.direction.y>1: # người chơi đang di chuyển xuống dưới, biểu thị sự sa ngã
            self.status='fall'
        else: #người chơi không di chuyển theo phương thẳng đứng (trên mặt đất hoặc đứng yên trên không).
            self.status = 'idle'

    # người chơi điều khiển chuyển động của nhân vật và thực hiện các hành động như nhảy.
    def get_input(self):
        keys=pygame.key.get_pressed() #truy xuất trạng thái của tất cả các phím trên bàn phím
        if keys[pygame.K_UP] : #phím lên
            self.jump()
        if keys[pygame.K_LEFT]:
            self.direction.x=-1 #hướng ngang của người chơi được đặt thành -1. biểu thị chuyển động sang trái
            self.facing_right=False
        elif keys[pygame.K_RIGHT]:
            self.direction.x=1 #hướng ngang của người chơi được đặt thành 1. biểu thị chuyển động sang phải
            self.facing_right = True
        else :
            self.direction.x=0 #hướng ngang của người chơi được đặt thành . Không có chuyển động

    def animate(self):
        # nhân vật của người chơi hiển thị các khung hoạt ảnh phù hợp dựa trên trạng thái hiện tại và hướng đối mặt của nhân vật đó.
        animation=self.animations[self.status] #lấy các khung hình động tương ứng với trạng thái hiện tại
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(animation): #frame_index vượt quá độ dài của khung hoạt hình
            self.frame_index=0 #được đặt lại thành 0 để lặp lại hoạt ảnh.
        image=animation[int(self.frame_index)] #Hình ảnh được lấy từ các khung hoạt hình dựa trên frame_index
        if self.facing_right==True:
            self.image=image
        else:
            self.image=pygame.transform.flip(image,True,False) #ình ảnh được lật theo chiều ngang
        #kiểm tra xem nhân vật của người chơi hiện đang ở trạng thái bất khả chiến bại hay không
        if self.invincible:
            value=self.Glitch() #phương thức Glitch được gọi để xác định giá trị alpha của hình ảnh.
            self.image.set_alpha(value)#Giá trị alpha kiểm soát độ trong suốt của hình ảnh.
        else: #nhân vật của người chơi không phải là bất khả chiến bại
            self.image.set_alpha(255) #giá trị alpha được đặt thành 255, có nghĩa là hình ảnh hoàn toàn mờ đục.
        #SET UP RECT
        # xác định vị trí và hướng của rect (hộp giới hạn) của nhân vật người chơi dựa trên tương tác của nó với mặt đất và trần nhà.
        if self.onGround and self.onLeft: # nhân vật của người chơi ở trên mặt đất và dựa vào bức tường bên trái
            self.rect=self.image.get_rect(bottomleft=self.rect.bottomleft) #vị trí của rect được đặt ở góc dưới cùng bên trái.
        elif self.onGround and self.onRight: #nhân vật của người chơi ở trên mặt đất và dựa vào bức tường bên phải
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright) #vị trí của rect được đặt ở góc dưới cùng bên phải.
        elif self.onGround : #nhân vật của người chơi ở trên mặt đất
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom) #vị trí của rect được đặt ở giữa dưới cùng.
        elif self.onCeiling and self.onLeft: #nhân vật của người chơi ở trên trần nhà và dựa vào bức tường bên trái
            self.rect = self.image.get_rect(topleft=self.rect.topleft) #vị trí của rect được đặt ở góc trên cùng bên trái.
        elif self.onCeiling and self.onRight: # nhân vật của người chơi ở trên trần nhà và dựa vào bức tường bên phải
            self.rect = self.image.get_rect(topright=self.rect.topright) #vị trí của rect được đặt ở góc trên cùng bên phải.
        elif self.onCeiling: # nhân vật của người chơi ở trên trần nhà
            self.rect = self.image.get_rect(midtop=self.rect.midtop) #vị trí của rect được đặt ở giữa trên cùng.
        #Bằng cách cập nhật vị trí của rect dựa trên tương tác của nhân vật với môi trường, các va chạm và chuyển động có thể được phát hiện và giải quyết chính xác.

    #cập nhật vị trí thẳng đứng của nhân vật người chơi và áp dụng trọng lực để mô phỏng việc rơi hoặc nhảy.
    def apply_gravity(self): #vị trí của nhân vật trên màn hình được điều chỉnh, tạo cảm giác như đang rơi hoặc nhảy.
        self.direction.y+=self.gravity #thể hiện tác động của trọng lực đối với chuyển động thẳng đứng của nhân vật.
        self.rect.y+=self.direction.y #hay đổi vị trí thẳng đứng của ký tự.

    #cho phép nhân vật của người chơi thực hiện hành động nhảy nếu đáp ứng một số điều kiện nhất định.
    def jump(self):
        if self.onGround==True and self.onCeiling!=True: #nhân vật của người chơi hiện đang ở trên mặt đất và không tiếp xúc với trần nhà
            #Giá trị self.jump_speed xác định vận tốc đi lên ban đầu của bước nhảy.
            self.direction.y=self.jump_speed # chuyển động thẳng đứng của nhân vật được đặt thành giá trị là self.jump_speed.
            self.jump_sound.play() #cung cấp phản hồi âm thanh cho hành động nhảy.

    # xử lý nhân vật của người chơi bị sát thương.
    def get_damed(self):
        if not self.invincible: #nhân vật hiện không phải là bất khả chiến bại
            self.change_health(-1) #sức khỏe của nhân vật sẽ giảm đi 1 bằng cách gọi hàm change_healthvới giá trị -1.
            self.invincible=True #nhân vật tạm thời bất khả chiến bại.
            self.hit_sound.play() # cung cấp phản hồi âm thanh khi nhận sát thương.
            self.hurt_time=pygame.time.get_ticks() #theo dõi thời gian nhân vật bị sát thương lần cuối, cho phép khoảng thời gian bất khả chiến bại tạm thời.

    #quản lý trạng thái bất khả chiến bại của nhân vật người chơi.
    def invincibility(self):
        if self.invincible: #nhân vật của người chơi hiện đang bất khả chiến bại
            currenTime=pygame.time.get_ticks() #kiểm tra thời gian đã trôi qua kể từ khi nhân vật bị hư hại lần cuối.
            if currenTime-self.hurt_time>=self.invincible_duration: # thời gian trôi qua vượt quá thời gian quy định
                self.invincible=False # thời gian bất khả chiến bại sẽ kết thúc và self.invinciblecờ được đặt thành False, cho phép nhân vật nhận lại sát thương.

    #tạo hiệu ứng trục trặc bằng cách điều chỉnh độ trong suốt (kênh alpha) của hình ảnh nhân vật người chơi dựa trên thời gian hiện tại.
    def Glitch(self):
        a = sin(pygame.time.get_ticks()) #lấy thời gian hiện tại tính bằng mili giây.áp dụng sinhàm từ mô-đun toán học cho giá trị thời gian hiện tại
        if a>=0 :return 255 #biểu thị độ mờ hoàn toàn.
        else:return 0 #biểu thị độ trong suốt hoàn toàn.
    #Điều này tạo ra hiệu ứng trục trặc trong đó hình ảnh của nhân vật xen kẽ giữa mờ hoàn toàn và hoàn toàn trong suốt dựa trên mẫu sóng hình sin.

    #chịu trách nhiệm cập nhật trạng thái và hoạt ảnh của người chơi
    def update(self):
        self.get_input() #kiểm tra đầu vào bàn phím và cập nhật hướng di chuyển của người chơi dựa trên các phím được nhấn.
        self.setup_status() #xác định trạng thái hiện tại của người chơi (không hoạt động, nhảy hoặc ngã) dựa trên hướng di chuyển của người chơi.
        self.animate() #cập nhật khung hoạt hình của người chơi dựa trên trạng thái hiện tại và hướng đối mặt.
        self.invincibility() #xử lý trạng thái và thời lượng bất khả chiến bại của người chơi, khiến người chơi dễ bị tổn thương trở lại sau một khoảng thời gian nhất định.









