# FlappyBird Game
# imports
import re
import pygame
import sys
import random
import time

# Start Game Module
pygame.init()


# All Variable
display_width = 349
display_height = 620
gravity = 0.25
bird_movment = 0
floor_x = 0
pipe_list = []
game_status = True
bird_list_index = 0
game_font = pygame.font.Font('assets/font/Flappy.TTF', 30)
score = 0
high_score = 0
active_score = True

#UserEvent#
create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_flap, 50)
pygame.time.set_timer(create_pipe, 1200)

#Sound
win_sound = pygame.mixer.Sound('assets/sound/smb_stomp.wav')
game_over_sound = pygame.mixer.Sound('assets/sound/smb_mario_die.wav')
#--------------------#
background_image = pygame.image.load('assets/img/bg3.png')
floor_image = pygame.image.load('assets/img/floor.png')
pipe_image = pygame.image.load('assets/img/pipe_red.png')
game_over_image = pygame.image.load('assets/img/message.png')
game_over_image_rect = game_over_image.get_rect(center= (174, 310))

bird_image_down = pygame.image.load('assets/img/red_bird_down_flap.png')
bird_image_mid = pygame.image.load('assets/img/red_bird_mid_flap.png')
bird_image_up = pygame.image.load('assets/img/red_bird_up_flap.png')

bird_list = [bird_image_up,  bird_image_mid, bird_image_down]

bird_image = bird_list[bird_list_index]



def generate_pipe_rect():
    random_pipe = random.randrange(240, 540)
    pipe_rect_top = pipe_image.get_rect(midbottom= (500, random_pipe - 135))
    pipe_rect_bottom = pipe_image.get_rect(midtop= (500, random_pipe))
    return pipe_rect_top, pipe_rect_bottom

def move_pipe_rect(pipes):
    for pipe in pipes:
        pipe.centerx -=4
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes

def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 620:
            main_screen.blit(pipe_image, pipe)
        else:
            reveresed_pipes = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(reveresed_pipes, pipe)


def check_collision(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
        if bird_image_rect.top <= -50 or bird_image_rect.bottom >= 550:
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
    return True


def bird_animition():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center = (80, bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(str(score), False, (255, 255, 255))
        text1_rect = text1.get_rect(center = (174, 60))
        main_screen.blit(text1, text1_rect)
    if status == 'game_over':
        #score
        text1 = game_font.render(f'Score: {score}', False, (255, 255, 255))
        text1_rect = text1.get_rect(center = (174, 60))
        main_screen.blit(text1, text1_rect)
        #high_score
        text2 = game_font.render(f'High Score: {high_score}', False, (255, 255, 255))
        text2_rect = text1.get_rect(center = (140, 520))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0:
                active_score = True

    if score > high_score:
        high_score = score
    return high_score


#-------------------#
bird_image_rect = bird_image.get_rect(center= (80, 300))
#-------------------#
# Game Display
main_screen = pygame.display.set_mode((display_width, display_height))


# Game Time
clock = pygame.time.Clock()

# Game Logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # End Game
            pygame.quit()
            # Terminate Program
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movment = 0
                bird_movment -= 6
            if event.key == pygame.K_r and game_status == False:
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (80, 300)
                bird_movment = 0
        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == create_flap:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0
            new_bird, new_bird_rect = bird_animition()
        
    
    
    # Display bg3.png
    main_screen.blit(background_image, (0, 0))      #(x, y)

    if game_status:
        #Check For Collision
        game_status = check_collision(pipe_list)

        # Display Bird Image
        main_screen.blit(new_bird, new_bird_rect)

        # Bird Gravity and Movment
        bird_movment += gravity
        bird_image_rect.centery += bird_movment

        # Display Pipe.png
        pipe_list = move_pipe_rect(pipe_list)
        display_pipes(pipe_list)

        #Show Score
        update_score()
        display_score('active')
    else:
        main_screen.blit(game_over_image, game_over_image_rect)
        score = 0
        display_score('game_over')
    # Display Floor.png
    floor_x -= 1
    main_screen.blit(floor_image, (floor_x, 550))
    main_screen.blit(floor_image, (floor_x + 349, 550))
    if floor_x <= -349:
        floor_x = 0

    pygame.display.update()
    # Set Game Speed
    clock.tick(90)