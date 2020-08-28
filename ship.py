import pygame
import random
from laser import Laser

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self, offset=(0,0), sound=None):
        offset_x, offset_y = offset
        if self.cool_down_counter == 0:
            laser = Laser(self.x - offset_x, self.y - offset_y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            if sound:
                sound.play()

    def move(self, vel):
        self.y += vel


class Player(Ship):
    
    def __init__(self, x, y, img, laser_img, health=100):
        Ship.__init__(self, x, y)
        self.ship_img = img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.health = health
        self.max_health = health

    def move_lasers(self, vel, objs, heigth):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(heigth):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
                            
        return 0

    def draw(self, window):
        Ship.draw(self, window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * self.health/self.max_health, 10))


class Enemy(Ship):

    def __init__(self, x, y, points, img):
        Ship.__init__(self, x, y)
        self.points = points
        self.ship_img, self.laser_img = img
        self.mask = pygame.mask.from_surface(self.ship_img)
        
    def move_lasers(self, vel, obj, height):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


class Life1up(Ship):

    def __init__(self, x, y, img):
        Ship.__init__(self, x, y)
        self.ship_img = img
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        vel_x = random.randrange(-5, 5)
        self.x += vel_x
        self.y += vel


class PowerShip(Ship):

    def __init__(self, x, y, img):
        Ship.__init__(self, x, y)
        self.ship_img = img
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        vel_x = random.randrange(-5, 5)
        self.x += vel_x
        self.y += vel
