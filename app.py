import pygame, sys
from pygame import mixer
from pygame.constants import K_f
from pygame.locals import *
from random import randint
import time



WIDTH = 854
HEIGHT = 480
RED = (255,0,0)
background = pygame.image.load('images/background2.png')
player_image = 'images/player.png'
bullet_image = 'images/bullet.png'
enemy_image = 'images/enemy.png'
power_up_image1 = 'images/powerup01.png'

pygame.mixer.init()
power_up_sfx = mixer.Sound('sounds/power_up_sfx.wav')



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player_image)
        self.image = pygame.transform.scale(self.image, (15*5, 15*5))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.speed = 7
        self.life = 5
        self.upgrade = 0
        self.wait = 300 #milisseconds
        self.last_shot = pygame.time.get_ticks()
        self.bullet_sfx = mixer.Sound('sounds/sound.wav')

    def update(self):
        
        #CHECK FOR KEYS EVENT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            player.rect.x += self.speed
        if keys[pygame.K_UP]:
            player.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            player.rect.y += self.speed

        #CURENT TIME
        current_time = pygame.time.get_ticks()

        #SHOOT BULLETS
        if keys[pygame.K_SPACE] and current_time - self.last_shot > self.wait:
            self.bullet_sfx.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_sprites.add(bullet)
            self.last_shot = current_time
            

        #MOVE LIMIT
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(bullet_image)
        self.image = pygame.transform.scale(self.image, (5*2, 5*2))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        if player.upgrade == 1:
            self.speed = 10
            player.wait = 200
        else:
            self.speed = 5
            player.wait = 300


    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(enemy_image)
        self.image = pygame.transform.scale(self.image, (15*5, 15*5))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = randint(15, WIDTH), 0
            player.life -= 1

        #MOVE LIMIT
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, image_file, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        self.speed = 3
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            self.kill()
        
        #MOVE LIMIT
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fps = pygame.time.Clock()
    global myfont
    myfont = pygame.font.SysFont("monospace", 26)
    timer = False
    timer_count = 1000


    #PLAYER SECTION
    player_sprites = pygame.sprite.Group()
    global player
    player = Player(WIDTH/2, HEIGHT - 100)
    player_sprites.add(player)

    #BULLETS SECTION
    global bullet_sprites
    bullet_sprites = pygame.sprite.Group()

    #ENEMIES SECTION
    enemy_sprites = pygame.sprite.Group()
    enemy = Enemy(randint(0, WIDTH), 0)
    # enemy2 = Enemy(randint(0, WIDTH), 0)
    enemy_sprites.add(enemy)


    #POWER UP SECTION
    power_up_sprites = pygame.sprite.Group()
    power_up_fast_bullets = Upgrade(power_up_image1, randint(0, WIDTH), 0)
    power_up_sprites.add(power_up_fast_bullets)




    global enemy_hit_sfx
    global point
    point = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_g:
                    player.upgrade = 0
                    
                if event.key == K_f:
                    player.upgrade = 1
                    power_up_sfx.play()
                        
        #COLLISION SECTION
        sprite_hit = pygame.sprite.spritecollide(player, enemy_sprites, False)
        

        power_up_hit = pygame.sprite.groupcollide(player_sprites, power_up_sprites, False, True)

        for hit in power_up_hit:
            player.upgrade = 1
            power_up_sfx.play()
            timer = True

        if timer == True:
            timer_count -= 1
        if timer_count <= 0:
            player.upgrade = 0
            timer = False


        
        for hit in sprite_hit:
            enemy_hit_sfx = mixer.Sound('sounds/enemy_hit_sfx.wav')
            enemy_hit_sfx.play()
            enemy.rect.center = randint(15, WIDTH), 0
            player.life -= 1

        bullet_hit = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, False)
        for hit in bullet_hit:
            enemy_hit_sfx = mixer.Sound('sounds/enemy_hit_sfx.wav')
            enemy_hit_sfx.play()
            enemy.rect.center = randint(15, WIDTH), 0
            point += 1


        fps.tick(60)

        screen.blit(background, (0,0))
        #DRAW PLAYER
        player_sprites.draw(screen)
        player_sprites.update()
        #DRAW BULLETS
        bullet_sprites.draw(screen)
        bullet_sprites.update()

        #DRAW ENEMIES
        enemy_sprites.draw(screen)
        enemy_sprites.update()

        #DRAW POWER UPS
        if point >= 15:
            power_up_sprites.draw(screen)
            power_up_sprites.update()

        if player.life <= 0:
            game_over()

            
            

        if player.life >= 3:
            lifes_label = myfont.render(f'{player.life}', 1, (0, 255, 0))
            screen.blit(lifes_label, (5, 3))
        if player.life < 3:
            lifes_label = myfont.render(f'{player.life}', 1, (255, 0, 0))
            screen.blit(lifes_label, (5, 3))

        point_label = myfont.render(f'{point}', 1, (0,0,255))
        screen.blit(point_label, (WIDTH - 50, 0))
        pygame.display.flip()



def game_over():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fps = pygame.time.Clock()

    while True:
        screen.fill(RED)
        gameover_label = myfont.render(f'GAME OVER! you killed {point} aircrafts.', 1, (255, 255, 0))
        play_again_label = myfont.render('Press ESC to play again.', 1, (255,255,0))
        screen.blit(play_again_label, (WIDTH / 2 - 200,  HEIGHT / 2 + 60))
        screen.blit(gameover_label, (WIDTH / 2 - 300, HEIGHT / 2))
        enemy_hit_sfx.stop()
        player.bullet_sfx.stop()
        power_up_sfx.stop()
        fps.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main()
        
        pygame.display.flip()
        

main()



