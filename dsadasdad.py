import pygame
from pygame.locals import *
import random

pygame.init()
q = 0
clock = pygame.time.Clock()
fps = 60

width = 700
height = 700
bird_group = pygame.sprite.Group()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')
pipe_group = pygame.sprite.Group()
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency

background_image = pygame.image.load('game_background1.png')
ground_image = pygame.image.load('ground.png')


class FlappyBird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.list_of_images = []
        self.ind = 0
        self.count = 0
        for number_of_image in range(1, 4):
            img = pygame.image.load(f'flappy_bird{number_of_image}.png')
            self.list_of_images.append(img)
        self.image = self.list_of_images[self.ind]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velichina = 0
        self.click = False

    def update(self):

        if flying == True:

            self.velichina += 0.5
            if self.velichina > 8:
                self.velichina = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.velichina)

        if game_over == False:

            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                self.velichina = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

            self.count += 1
            jump_cooldown = 5

            if self.count > jump_cooldown:
                self.count = 0
                self.ind += 1
                if self.ind >= len(self.list_of_images):
                    self.ind = 0
            self.image = self.list_of_images[self.ind]

            self.image = pygame.transform.rotate(self.list_of_images[self.ind], self.velichina * -2)
        else:
            self.image = pygame.transform.rotate(self.list_of_images[self.ind], -90)


flappy = FlappyBird(100, int(height / 2))
bird_group.add(flappy)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


run = True
while run:

    clock.tick(fps)

    screen.blit(background_image, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    screen.blit(ground_image, (ground_scroll, 600))
    pipe_group.draw(screen)

    if flappy.rect.bottom > 600:
        game_over = True
        flying = False

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        background_image = pygame.image.load('game_background2.png')

    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(width, int(height / 2) + pipe_height, -1)
            top_pipe = Pipe(width, int(height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if flying == False and game_over == False:
                if x >= 225 and x <= 465 and y >= 269 and y <= 390:
                    background_image = pygame.image.load('game_background.png')
                    q = 1
                if q == 1:
                    flying = True
                elif x >= 525 and x <= 615 and y >= 292 and y <= 361:

            if flying == False and game_over == True:
                if x >= 225 and x <= 465 and y >= 269 and y <= 390:
                    background_image = pygame.image.load('game_background.png')
                    screen.blit(ground_image, (ground_scroll, 600))
                    screen.blit(background_image, (0, 0))
                    bird_group = pygame.sprite.Group()
                    pipe_group = pygame.sprite.Group()
                    flying = True
                    game_over = False
                    last_pipe = pygame.time.get_ticks() - pipe_frequency
                    q = 0
                    flappy = FlappyBird(100, int(height / 2))
                    bird_group.add(flappy)
    pygame.display.update()

pygame.quit()
