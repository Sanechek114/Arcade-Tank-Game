import arcade
from config import (SCALE, SCREEN_WIDTH, SCREEN_HEIGHT, LIVES,
                    MAX_SPEED,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, RELOUDTIME)
import math
from bullet_class import Bullet


class Tank_hull(arcade.Sprite):
    def __init__(self, path, max_speed):
        super().__init__(path, center_x=100, center_y=200, scale=SCALE)
        self.max_speed = max_speed
        self.speed = 0

    def update(self, delta_time, control):
        forward, backward, right, left = control

        if forward and not backward:
            self.speed += (self.max_speed - self.speed) * delta_time

        elif not forward and backward:
            self.speed += (-self.max_speed - self.speed) * delta_time

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
    def __init__(self, path, bullet_path, bullets, hull, reloudtime, turret_id):
        super().__init__(path, center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.bullet_path = bullet_path
        self.shoot_sound = arcade.load_sound("assets/sounds/shoot.mp3")
        self.bullets = bullets
        self.hull = hull
        bullet_modifers = {1: (1, 1),
                           2: (3, 0.5),
                           3: (2, 1.5)}
        self.bullet_damage, self.bullet_speed = bullet_modifers[turret_id]
        self.reloudtimer = 0
        self.reloudtime = reloudtime

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
        if 0 < abs((mouse_angle - self.angle + 180) % 360) < 180:
            self.angle += TURRETROTATIONSPEED * delta_time
        if 360 > abs((mouse_angle - self.angle + 180) % 360) > 180:
            self.angle -= TURRETROTATIONSPEED * delta_time

        Tx = Hx - (11) * SCALE * math.sin(
            math.radians((self.angle) % 360))
        Ty = Hy - (11) * SCALE * math.cos(
            math.radians((self.angle) % 360))
        self.position = Tx, Ty

    def tank_shooting(self, delta_time, fire):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.5)
            self.reloudtimer = self.reloudtime
            x, y = self.center_x, self.center_y
            angle = self.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle)),
                      y + -SCALE * 10 * math.cos(math.radians(angle)))
            newBullet = Bullet(
                self.bullet_path, Bx, By, angle - 180, self.bullet_speed,
                self.bullet_damage, self.bullets, True)
            self.bullets.append(newBullet)


class Player(arcade.SpriteList):
    def __init__(self, color, turret_id, bullets, walls):
        super().__init__()
        self.bullets = bullets
        self.walls = walls
        self.tank_color = color
        self.turret_id = turret_id
        # color: reloud time, lives, speed
        modifications = {'red': (
                             RELOUDTIME, LIVES, MAX_SPEED),
                         'blue': (
                             RELOUDTIME // 1.5, LIVES, MAX_SPEED // 2),
                         'green': (
                             RELOUDTIME * 1.5, LIVES * 2, MAX_SPEED),
                         'sand': (
                             RELOUDTIME, LIVES // 2, MAX_SPEED * 1.5)}

        reloudtime, self.lives, max_speed = modifications[color]
        self.turret_path = f"assets/sprites/barrels/tank{color.capitalize()}_barrel{turret_id}.png"
        self.hull_path = f"assets/sprites/bodyes/tankBody_{color}_outline.png"
        self.bullet_path = f"assets/sprites/bullets/bullet{color.capitalize()}{turret_id}_outline.png"

        self.hull = Tank_hull(self.hull_path, max_speed)
        self.turret = Tank_turret(self.turret_path, self.bullet_path, bullets, self.hull, reloudtime, turret_id)
        self.append(self.hull)
        self.append(self.turret)

    def get_lives_relouding(self):
        return (self.lives, self.turret.reloudtime,
                self.turret.reloudtimer)

    def update(self, delta_time, control):
        self.hull.update(delta_time, control[:4])
        self.turret.update(delta_time, control[4:])
