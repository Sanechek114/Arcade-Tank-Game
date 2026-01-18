import arcade
from config import (SCALE, SCREEN_WIDTH, SCREEN_HEIGHT, LIVES,
                    BRAKINGFORCE, MAX_SPEED, ACCELERATION,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, RELOUDTIME)
import math
from bullet_class import Bullet


class Tank_hull(arcade.Sprite):
    def __init__(self, ):
        super().__init__(center_x=100, center_y=200, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/bodyes/tankBody_blue_outline.png')
        self.speed = 0

    def update(self, delta_time, control):
        forward, backward, right, left = control

        if forward and not backward:
            self.speed += (MAX_SPEED - self.speed) * delta_time

        elif not forward and backward:
            self.speed += (-MAX_SPEED - self.speed) * delta_time

        else:
            self.speed += (0 - self.speed) * delta_time

        if right and not left:
            self.angle = self.angle + HULLROTATIONSPEED * delta_time

        if not right and left:
            self.angle = self.angle - HULLROTATIONSPEED * delta_time

        self.change_x = self.speed * math.sin(
            math.radians(self.angle + 180)) * delta_time
        self.change_y = self.speed * math.cos(
            math.radians(self.angle + 180)) * delta_time

        #  self.position = (self.center_x + self.change_x, self.center_y + self.change_y)


class Tank_turret(arcade.Sprite):
    def __init__(self, bullets, hull):
        super().__init__(center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/barrels/tankBlue_barrel2_outline.png')
        self.shoot_sound = arcade.load_sound("assets/sounds/shoot.mp3")
        self.bullets = bullets
        self.hull = hull
        self.reloudtimer = 0

    def update(self, delta_time, control):
        self.turret_update(delta_time, control[1])
        self.tank_shooting(delta_time, control[0])

    def turret_update(self, delta_time, mouseXY):
        Wx, Wy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        Mx, My = mouseXY
        Hx, Hy = self.hull.position
        atan = math.atan2(-Wx + Mx, -Wy + My)
        if atan < 0:
            atan += 2 * math.pi
        mouse_angle = math.degrees(atan)
        if 0 < abs((mouse_angle - self.angle + 360 + 180) % 360) < 180:
            self.angle += TURRETROTATIONSPEED * (self.speed) * delta_time
        if 360 > abs((mouse_angle - self.angle + 360 + 180) % 360) > 180:
            self.angle -= TURRETROTATIONSPEED * (self.speed) * delta_time

        Tx = Hx - (11) * SCALE * math.sin(
            math.radians((self.angle) % 360))
        Ty = Hy - (11) * SCALE * math.cos(
            math.radians((self.angle) % 360))
        self.position = Tx, Ty

    def tank_shooting(self, delta_time, fire):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.5)
            self.reloudtimer = RELOUDTIME
            x, y = self.center_x, self.center_y
            angle = self.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle)),
                      y + -SCALE * 10 * math.cos(math.radians(angle)))
            newBullet = Bullet(Bx, By, angle, self.bullets, True)
            self.bullets.append(newBullet)


class Player(arcade.SpriteList):
    def __init__(self, color, turret, bullets, walls):
        super().__init__()
        self.bullets = bullets
        self.walls = walls
        self.color = color
        self.turret = turret
        # color: reloud time, lives, speed
        modifications = {'red': (
                             RELOUDTIME, LIVES, MAX_SPEED),
                         'blue': (
                             RELOUDTIME // 2, LIVES, MAX_SPEED // 2),
                         'green': (
                             RELOUDTIME * 2, LIVES * 2, MAX_SPEED),
                         'yellow': (
                             RELOUDTIME, LIVES // 2, MAX_SPEED * 2)}

        self.modification = modifications[color]

        self.turret = {'red': }

        self.hull = Tank_hull()
        self.turret = Tank_turret(bullets, self.hull)
        self.append(self.hull)
        self.append(self.turret)
        self.lives = 3

    def update(self, delta_time, control):
        self.hull.update(delta_time, control[:4])
        self.turret.update(delta_time, control[4:])
