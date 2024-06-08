import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('images/1.png'))

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)

imgBG = pygame.image.load('images/background.png')
imgbird = pygame.image.load('images/0.png')
imgPT = pygame.image.load('images/top.png')
imgPB = pygame.image.load('images/bottom.png')

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 40, 30)
frame = 0

state = 'start'
timer = 10

pipes = []
bges = []
pipescores = []

pipespeed = 3
pipegatesize = 200
pipeGatePos = HEIGHT // 2

bges.append(pygame.Rect(0, 0, 390, 708))

lives = 3
scores = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: play = False
    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer: timer -= 1

    frame = (frame + 0.2) % 3

    for i in range(len(bges)-1, -1, -1):
        bg = bges[i]
        bg.x -= pipespeed // 2

        if bg.right < 0: bges.remove(bg)

        if bges[-1].right <= WIDTH: bges.append(pygame.Rect(bges[-1].right, 0, 390, 708))


    for i in range(len(pipes)-1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipespeed

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in pipescores: pipescores.remove(pipe)

    if state == 'start':
        if click and not timer and not len(pipes): state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    elif state == 'play':
        if click: ay = -2
        else: ay = 0

        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if not len(pipes) or pipes[-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 98, pipeGatePos - pipegatesize // 2))
            pipes.append(pygame.Rect(WIDTH, pipeGatePos + pipegatesize // 2, 98, HEIGHT - pipeGatePos + pipegatesize // 2))

            pipeGatePos += randint(-100,100)
            if pipeGatePos < pipegatesize: pipeGatePos = pipegatesize
            elif pipeGatePos > HEIGHT - pipegatesize: pipeGatePos = HEIGHT - pipegatesize

        if player.top < 0 or player.bottom > HEIGHT: state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe): state = 'fall'

            if pipe.right < player.left and pipe not in pipescores:
                pipescores.append(pipe)
                scores += 5
                pipespeed = 3 + scores // 100

    elif state == 'fall':
        sy, ay = 0, 0
        pipeGatePos = HEIGHT // 2

        lives -= 1
        if lives:
            state = 'start'
            timer = 60
        else:
            state = 'game over'
            timer = 150


    else:
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if not timer: play = False

    for bg in bges: window.blit(imgBG, bg)

    for pipe in pipes:
        if not pipe.y:
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft = pipe.topleft)
            window.blit(imgPB, rect)



    image = imgbird.subsurface(40 * int(frame), 0, 40, 30)
    image = pygame.transform.rotate(image, -sy * 2.5)
    window.blit(image, player)

    text = font1.render('Очки: ' + str(scores), 1, pygame.Color('black'))
    window.blit(text, (10,10))

    text = font1.render('Жизни: ' + str(lives), 1, 'black')
    window.blit(text, (10, HEIGHT - 30))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()