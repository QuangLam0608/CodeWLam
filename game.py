import pygame, sys, random

#TẠO HÀM CHO GAME
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

#Hàm xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): #chạm vào ống
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650: #vượt quá cửa sổ pygame or chạm sàn
            return False
    return True 

#Hàm tạo chuyển động cho chim (lên xuống)
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1) #rotozoom tạo hiệu ứng xoay cho chim
	return new_bird

#Hàm tạo hiệu ứng đập cánh
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (350,bird_rect.centery))
    return new_bird, new_bird_rect

#Hàm hiển thị điểm
def score_display(game_state):
    if game_state == 'main game': #khi game active
        score_surface = game_font.render(str(int(score)),True,(128,0,0))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over': #khi game over
        score_surface = game_font.render(f'Score: {int(score)}',True,(128,0,0))
        score_rect = score_surface.get_rect(center = (648,100))
        screen.blit(score_surface,score_rect)
 
        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(128,0,0))
        high_score_rect = high_score_surface.get_rect(center = (648,630))
        screen.blit(high_score_surface,high_score_rect)

#Hàm update highscore
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((1296,768)) #Tạo màn hình chính của game 
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

#Tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

#chèn background
bg = pygame.image.load('assets/bgtet.jpg').convert() #convert giúp đổi file hình thành một file nhẹ hơn giúp load lẹ hơn

#chèn sàn
floor = pygame.image.load('assets/floortet.jpg').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (350,384)) #get_reck để tạo một hình chữ nhật xung quanh chim

#tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)

#tạo ống
pipe_surface = pygame.image.load('assets/pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[] #chứa ống đã tạo ra

#tạo timer (cho ống xuất hiện liên tục)
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1000)
pipe_height = [200,250,300,350,400,450,500] #chiều cao ống ngẫu nhiên

#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(648,384))

#Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/vitkeu.mp3')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

#while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: #khi game active
                bird_movement = 0
                bird_movement =-7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False: #khi game over thì bấm spacebar game active lại
                game_active = True 
                pipe_list.clear() #reset list ống
                bird_rect.center = (350,384)
                bird_movement = 0 
                score = 0
        #ống
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) 
        #hiệu ứng chuyển động chim
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation()    
            
    screen.blit(bg,(0,0))

    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)       
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active= check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    #sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0
    
    pygame.display.update()
    clock.tick(120)
