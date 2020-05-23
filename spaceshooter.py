from ship import Player, Enemy, Life1up, PowerShip
from record import checkRecord
from collide import collide
import time
import pygame
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Shooter')

# Load Images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

# 1UP an Power icon
LIFE_1UP = pygame.image.load(os.path.join('assets', '1up.png'))
POWER_UP = pygame.image.load(os.path.join('assets', 'power.png'))

# Lasers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

# Sounds
pygame.mixer.init(44100, -16, 2, 2048)
SHOOT = pygame.mixer.Sound(os.path.join('music', 'shoot.wav'))
#LIFE_1UP_SOUND = pygame.mixer.Sound(os.path.join('music', '1Up.wav'))

# Maps for Enemies
MAP_ENEMY = {
        'red': (RED_SPACE_SHIP, RED_LASER, 20),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER, 30),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER, 50)
    }


def main():
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.mixer.music.load(os.path.join('music', 'Saturn.mp3'))
    pygame.mixer.music.play(-1)
    
    FPS = 60
    run = True
    level = 0
    lives = 5
    score = 0
    lost = False
    lost_count = 0
    main_font = pygame.font.SysFont('comicsans', 40)

    enemies = []
    lives1up = []
    powers = []
    picked_pow = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5
    life1up_vel = 6
    power_vel = 6

    player = Player(300, 650, img=YELLOW_SPACE_SHIP, laser_img=YELLOW_LASER)
    player_vel = 10
    player_laser_vel = 15


    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))

        # Draw Text
        lives_label = main_font.render('Lives: {}'.format(lives), 1, (255, 255, 255))
        level_label = main_font.render('Level: {}'.format(level), 1, (255, 255, 255))
        score_label = main_font.render('Score: {}'.format(score), 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, HEIGHT - score_label.get_height()))

        for enemy in enemies:
            enemy.draw(WIN)
        for life1up in lives1up:
            life1up.draw(WIN)
        for power in powers:
            power.draw(WIN)
        player.draw(WIN)

        for x in range(len(picked_pow)):
            WIN.blit(POWER_UP, (WIDTH - POWER_UP.get_width()*(x+1) - 10, HEIGHT - POWER_UP.get_width()))
        
        if lost:
            lost_label = main_font.render('Game Over!', 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                c = random.choice(['red', 'blue', 'green'])
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), points=MAP_ENEMY[c][2], img=MAP_ENEMY[c][:2])
                enemies.append(enemy)

        # Life Up arrival
        if random.randrange(0, 1000) == 1:
            life1up = Life1up(random.randrange(50, WIDTH-100),random.randrange(-1500, -100), img=LIFE_1UP)
            lives1up.append(life1up)

        # Power energy arrival
        if random.randrange(0, 800) == 1:
            power = PowerShip(random.randrange(50, WIDTH-100),random.randrange(-1500, -100), img=POWER_UP)
            powers.append(power)

        # Key press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(offset=(20,50), sound=SHOOT)
                if event.key == pygame.K_p:
                    if len(picked_pow) > 0 and player.health < 100:
                        picked_pow.remove(picked_pow[0])
                        player.health = 100
                        
        # Movemnts
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: 
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel

        # Check if Enemies
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player, HEIGHT)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot(offset=(15, 0))
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
                
        # Check Life 1UP
        for life1up in lives1up[:]:
            life1up.move(life1up_vel)
            if collide(life1up, player):
                #LIFE_1UP_SOUND.play()
                lives += 1
                lives1up.remove(life1up)
            elif life1up.y + life1up.get_height() > HEIGHT:
                lives1up.remove(life1up)
        
        # Check Power Energy
        for power in powers[:]:
            power.move(power_vel)
            if collide(power, player):
                if len(picked_pow) < 7:
                    picked_pow.append(power)
                powers.remove(power)
            elif power.y + power.get_height() > HEIGHT:
                powers.remove(power)

        score += player.move_lasers(-player_laser_vel, enemies, HEIGHT)
    
    return False, level, score

def displayStanding(standing, font):
    WIN.blit(BG, (0, 0))
    for i, line in enumerate(standing):
        offset = 50
        for word in line.split('\t'):
            word_label = font.render(word, 1, (255, 255, 255))
            WIN.blit(word_label, (offset + word_label.get_width(), HEIGHT/2 + (i+1) * word_label.get_height()))
            offset += 2*word_label.get_width()
    pygame.display.update()

def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    standing_font = pygame.font.SysFont('comicsans', 35)
    name = input('Chi sta giocando, inserisci il nome [3 caratteri]: ')
    run = True
    start = True

    while run:
        if start:
            WIN.blit(BG, (0, 0))
            title_label = title_font.render('Press P to play...', 1, (255, 255, 255))
            WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        start, level, score = main()
        else:
            dmy = time.strftime("%d-%m-%Y")
            standing = checkRecord(level=level, points=score, date=dmy, name=name[:3]).split('\n')
            displayStanding(standing, standing_font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    pygame.quit()


main_menu()


