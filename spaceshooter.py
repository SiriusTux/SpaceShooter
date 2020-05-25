from ship import Player, Enemy, Life1up, PowerShip
from record import checkRecord, getBestScore
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
RED_SPACE_SHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_blue_small.png'))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_yellow.png'))

# 1UP an Power icon
LIFE_1UP = pygame.image.load(os.path.join('assets', '1up.png'))
POWER_UP = pygame.image.load(os.path.join('assets', 'power.png'))

# Lasers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(
    os.path.join('assets', 'pixel_laser_green.png'))
YELLOW_LASER = pygame.image.load(
    os.path.join('assets', 'pixel_laser_yellow.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

# Sounds
pygame.mixer.init(44100, -16, 2, 2048)
SHOOT = pygame.mixer.Sound(os.path.join('music', 'shoot.wav'))
#LIFE_1UP_SOUND = pygame.mixer.Sound(os.path.join('music', '1Up.wav'))

# Colors
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIME = (0, 255, 0)


# Maps for Enemies
MAP_ENEMY = {
    'red': (RED_SPACE_SHIP, RED_LASER, 20),
    'green': (GREEN_SPACE_SHIP, GREEN_LASER, 30),
    'blue': (BLUE_SPACE_SHIP, BLUE_LASER, 50)
}


def main(name):
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.mixer.music.load(os.path.join('music', 'Saturn.mp3'))
    pygame.mixer.music.play(-1)

    FPS = 60
    run = True
    level = 0
    lives = 5
    best = getBestScore()
    score = 0
    lost = False
    lost_count = 0
    main_font = pygame.font.Font(os.path.join('font', 'PressStart2P-Regular.ttf'), 20)

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
        WIN.blit(BG, (0, 0))

        # Draw Text on screen
        lives_label = main_font.render(
            'Lives:{}'.format(lives), 1, WHITE)
        level_label = main_font.render(
            'Level:{}'.format(level), 1, CYAN)
        best_label = main_font.render('WR:{}'.format(best), 1, MAGENTA)
        score_label = main_font.render(
            '{}:{}'.format(name, score), 1, LIME)
        WIN.blit(score_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(best_label, (WIDTH/2 - best_label.get_width()/2, 10))
        WIN.blit(lives_label, (10, HEIGHT - lives_label.get_height()))

        for enemy in enemies:
            enemy.draw(WIN)
        for life1up in lives1up:
            life1up.draw(WIN)
        for power in powers:
            power.draw(WIN)
        player.draw(WIN)

        for x in range(len(picked_pow)):
            WIN.blit(POWER_UP, (WIDTH - POWER_UP.get_width() *
                                (x+1) - 10, HEIGHT - POWER_UP.get_width()))

        if lost:
            lost_label = main_font.render('Game Over!', 1, WHITE)
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
            life1up = Life1up(random.randrange(50, WIDTH-100),
                              random.randrange(-1500, -100), img=LIFE_1UP)
            lives1up.append(life1up)

        # Power energy arrival
        if random.randrange(0, 800) == 1:
            power = PowerShip(random.randrange(50, WIDTH-100),
                              random.randrange(-1500, -100), img=POWER_UP)
            powers.append(power)

        # Key press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(offset=(20, 50), sound=SHOOT)
                if event.key == pygame.K_RCTRL:
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

        # Check if player score is better than World Record
        if score >= best:
            best = score

    return False, level, score


def displayStanding(standing, font, score):
    WIN.blit(BG, (0, 0))
    # Display Hall of Fame title
    font_hall = pygame.font.Font(os.path.join('font', 'PressStart2P-Regular.ttf'), 40)
    hall_of_fame_label = font_hall.render('Hall of Fame', 1, MAGENTA)
    WIN.blit(hall_of_fame_label, (WIDTH/2 - hall_of_fame_label.get_width()/2, HEIGHT / 4))
    # Display first line of standings
    title = ('rank', 'name', 'lev', 'score', 'date')
    title_line = '{:>5}{:>5}{:>5}{:>10}{:>15}'.format(*title)
    title_line_label = font.render(title_line, 1, (255, 255, 255))
    WIN.blit(title_line_label, ((WIDTH - title_line_label.get_width())/2, HEIGHT/2 - title_line_label.get_height()))
    # Display each row of standings
    for i, line in enumerate(standing):
        standing_line = '{:^5}{:^5}{:>5}{:>10}{:>15}'.format(*line.split('\t'))
        if int(line.split('\t')[3]) == score:
            # Change color on actual game score if in standings
            standing_line_label = font.render(standing_line, 1, LIME)
        else:
            standing_line_label = font.render(standing_line, 1, WHITE)
        WIN.blit(standing_line_label, ((WIDTH - standing_line_label.get_width())/2, HEIGHT/2 + (i+1) * standing_line_label.get_height()))
    pygame.display.update()

def displayStartScreen(font, text):
    WIN.blit(BG, (0, 0))
    welcome_mes = font.render('Welcome to Space Shooter!', 1, MAGENTA)
    please_font = pygame.font.Font(os.path.join('font', 'PressStart2P-Regular.ttf'), 20)
    please_mes = please_font.render('Enter your name', 1, WHITE)
    WIN.blit(welcome_mes, (WIDTH/2 - welcome_mes.get_width()/2, HEIGHT/4))
    WIN.blit(please_mes, (WIDTH/2- please_mes.get_width()/2, 3*HEIGHT/8))
    input_points = font.render('....', 1, LIME)
    txt_surface = font.render(text, True, LIME)
    WIN.blit(input_points, (WIDTH/2 - input_points.get_width()/2, HEIGHT/2+10))
    WIN.blit(txt_surface, (WIDTH/2 - 76/2, HEIGHT/2))
    pygame.display.update()


def main_menu():
    title_font = pygame.font.Font(os.path.join(
        'font', 'PressStart2P-Regular.ttf'), 25)
    standing_font = pygame.font.Font(os.path.join(
        'font', 'PressStart2P-Regular.ttf'), 17)
    run = True
    start = True
    blink = 1
    name_ok = False
    text = ''

    while run:
        if start:
            ### Game Start ###
            if not name_ok:
                displayStartScreen(title_font, text)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if len(text) < 3:
                        if event.type == pygame.KEYDOWN:
                            #if active:
                            if event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            else:
                                text += event.unicode
                    else:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            elif event.key == pygame.K_RETURN:
                                name = text
                                name_ok = True
            else:
                displayStartScreen(title_font, text)
                blink += 1
                title_label = title_font.render('Press P to play...', 1, WHITE)
                if blink % 2 == 0:
                    WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 3*HEIGHT/4))
                pygame.time.wait(250)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            start, level, score = main(name)
        else:
            ### Game Over ###
            dmy = time.strftime("%d-%m-%Y")
            standing = checkRecord(
                level=level, points=score, date=dmy, name=name[:3]).split('\n')
            displayStanding(standing, standing_font, score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    pygame.quit()


main_menu()

