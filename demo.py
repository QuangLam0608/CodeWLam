import pygame, sys, random 

#Hàm tạo sàn (tạo 4 sàn nối tiếp nhau)
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
    screen.blit(floor,(floor_x_pos+864,650))
    screen.blit(floor,(floor_x_pos+1296,650))

#Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) #vị trí ống ngẫu nhiên
    bottom_pipe = pipe_surface.get_rect(midtop =(1200,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(1200,random_pipe_pos-720))
    return bottom_pipe, top_pipe

#Hàm di chuyển ống
def move_pipe(pipes):                  
	for pipe in pipes :
		pipe.centerx -= 7
	return pipes

#Hàm vẽ ống lên screen
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 : 
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True) 
            screen.blit(flip_pipe,pipe)


pygame.init()
screen = pygame.display.set_mode((1296,768)) #Tạo màn hình chính của game 
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

#Tạo các biến
gravity = 0.25
bird_movement = 0

#chèn background
bg = pygame.image.load('assets/bgtet.jpg').convert() #convert giúp đổi file hình thành một file nhẹ hơn giúp load lẹ hơn

#chèn sàn
floor = pygame.image.load('assets/floortet.jpg').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#tạo chim
#bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
#bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
#bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
#bird_list= [bird_down,bird_mid,bird_up] #0 1 2
#bird_index = 0
#bird = bird_list[bird_index]
bird = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_rect = bird.get_rect(center = (350,384)) #get_reck để tạo một hình chữ nhật xung quanh chim

#tạo ống
pipe_surface = pygame.image.load('assets/pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[] #chứa ống đã tạo ra

#tạo timer (cho ống xuất hiện liên tục)
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1000)
pipe_height = [200,250,300,350,400,450,500] #chiều cao ống ngẫu nhiên

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #khi game active
                bird_movement = 0
                bird_movement = -7
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) 
                
          
    screen.blit(bg,(0,0))
    #chim  
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird,bird_rect)
    #ống
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)
    #sàn
    floor_x_pos -= 1
    #screen.blit(floor,(floor_x_pos,600))
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)