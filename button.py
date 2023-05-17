import pygame


class Button():
	#cung cấp một cấu trúc cơ bản để tạo và xử lý các nút có thể nhấp được trong giao diện người dùng đồ họa. Hình thức, vị trí, văn bản và màu sắc của nút có thể được tùy chỉnh bằng cách đặt các thuộc tính thích hợp.
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image #Hình ảnh được liên kết với nút.
		self.x_pos = pos[0] #Tọa độ x và y của vị trí nút.
		self.y_pos = pos[1]
		self.font = font #Phông chữ được sử dụng cho văn bản của nút.
		self.base_color, self.hovering_color = base_color, hovering_color #Màu cơ bản và màu ẩn của nút.
		self.text_input = text_input #Văn bản đầu vào hiển thị trên nút.
		self.text = self.font.render(self.text_input, True, self.base_color) #Văn bản được hiển thị sử dụng phông chữ và màu cơ bản đã chỉ định.
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) # Hình chữ nhật bao quanh hình ảnh của nút
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos)) # Hình chữ nhật bao quanh văn bản của nút.
		self.get_hover = pygame.mixer.Sound('./audio/choose_sound.wav') # Âm thanh phát ra khi nút được di chuột qua.

	#ảm bảo rằng cả hình ảnh và văn bản của nút được hiển thị trên bề mặt màn hình được chỉ định làm đối số. Nó cho phép nút được cập nhật và hiển thị ở vị trí thích hợp với hình ảnh và văn bản liên quan.
	def update(self, screen): #Cập nhật và hiển thị nút trên screen bề mặt được chỉ định.
		if self.image is not None: #Nếu nút có hình ảnh
			screen.blit(self.image, self.rect) #làm mờ hình ảnh trên màn hình ở vị trí hình chữ nhật của nút ( self.rect).
		screen.blit(self.text, self.text_rect) #làm mờ văn bản của nút ( self.text) trên màn hình ở vị trí hình chữ nhật của văn bản ( self.text_rect).

	# cho phép bạn xác định xem nút đã được tương tác hay chưa bằng cách kiểm tra xem vị trí nhấp chuột hoặc chạm có nằm trong giới hạn của hình chữ nhật của nút hay không. Nếu đúng như vậy, phương thức sẽ trả về Trueđể cho biết rằng nút đã được nhấp hoặc chọn.
	def checkForInput(self, position): #Kiểm tra xem nút đã được nhấp hay chọn dựa trên giá trị đã cho position.
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): #kiểm tra xem tọa độ x của nút positioncó nằm trong phạm vi ngang của hình chữ nhật của nút ( self.rect.leftđến self.rect.right) và tọa độ y có nằm trong phạm vi dọc của hình chữ nhật của nút ( self.rect.topđến self.rect.bottom) hay không.
			self.get_hover.play(maxtime=1000) #Nếu vị trí nằm trong hình chữ nhật của nút, nó sẽ phát âm thanh ẩn
			return True #quay lại Trueđể cho biết rằng nút đã được nhấp hoặc chọn.
		return False #Nếu vị trí nằm ngoài hình chữ nhật của nút, nó sẽ quay lại Falseđể cho biết rằng nút chưa được nhấp hoặc chọn.

	#cho phép bạn thay đổi màu văn bản của nút dựa trên vị trí của con trỏ chuột hoặc đầu vào cảm ứng. Khi con trỏ hoặc thao tác chạm nằm trong hình chữ nhật của nút, văn bản sẽ được hiển thị bằng màu ẩn. Mặt khác, nó được hiển thị với màu cơ bản.
	def changeColor(self, position): #Thay đổi màu văn bản của nút dựa trên màu đã cho position.
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): #Nó kiểm tra xem tọa độ x của nút positioncó nằm trong phạm vi ngang của hình chữ nhật của nút ( self.rect.leftđến self.rect.right) và tọa độ y có nằm trong phạm vi dọc của hình chữ nhật của nút ( self.rect.topđến self.rect.bottom) hay không.
			self.text = self.font.render(self.text_input, True, self.hovering_color) #Nếu vị trí nằm trong hình chữ nhật của nút, nó sẽ cập nhật văn bản của nút để hiển thị bằng màu ẩn ( self.hovering_color) bằng cách tạo bề mặt văn bản hiển thị mới với màu ẩn đã chỉ định.
		else:
			self.text = self.font.render(self.text_input, True, self.base_color) #cập nhật văn bản của nút để hiển thị bằng màu cơ bản ( self.base_color) bằng cách tạo bề mặt văn bản hiển thị mới với màu cơ bản đã chỉ định.

