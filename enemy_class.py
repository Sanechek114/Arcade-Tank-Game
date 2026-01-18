import arcade
from config import (SCALE, ENEMY_VIEW, MAX_SPEED,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, RELOUDTIME)
from bullet_class import Bullet
import math
from explosion import Explosion


class Tank_hull(arcade.Sprite):
    def __init__(self, player):
        super().__init__(scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/bodyes/enemy/tankBody_1.png')
        self.player = player
        self.speed = MAX_SPEED / 3
        self.on_point = True
        self.player_point = self.position
        self.target_angle = self.angle
        self.lives = 1

    def next_point(self, player_in_sight):
        Hx, Hy = self.position
        if player_in_sight:
            Px, Py = self.player.position
            Hx, Hy = self.position
            atan = math.atan2((-Px + Hx),
                              (-Py + Hy))
            if atan < 0:
                atan += 2 * math.pi
            self.target_angle = math.degrees(atan) % 360
            self.player_point = self.player.position
        self.on_point = math.sqrt(
            (self.player_point[0] - Hx) ** 2 + \
            (self.player_point[1] - Hy) ** 2) < 100 * SCALE

    def update(self, delta_time, player_in_sight):
        self.next_point(player_in_sight)
        self.enemy_rotate(delta_time)
        if abs(self.target_angle - self.angle) % 360 <= 60:
            self.position = (self.center_x + self.change_x,
                             self.center_y + self.change_y)

    def enemy_rotate(self, delta_time):
        if 0 < abs((self.target_angle - self.angle + 360) % 360) < 180:
            self.angle += HULLROTATIONSPEED / 1.5 * delta_time
        if 360 > abs((self.target_angle - self.angle + 360) % 360) > 180:
            self.angle -= HULLROTATIONSPEED / 1.5 * delta_time
        if not self.on_point:
            print('Move')
            print(abs(self.target_angle - self.angle) % 360)
            self.change_x = self.speed * math.sin(
                math.radians(self.angle + 180)) * delta_time
            self.change_y = self.speed * math.cos(
                math.radians(self.angle + 180)) * delta_time
        else:
            self.change_x, self.change_y = 0, 0


class Tank_turret(arcade.Sprite):
    def __init__(self, player, bullets):
        super().__init__(center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/barrels/enemy/specialBarrel1.png')
        self.shoot_sound = arcade.load_sound("assets/sounds/awp.mp3")
        self.bullet_path = 'assets/sprites/bullets/enemy/bulletDark1_outline.png'
        self.player = player
        self.bullets = bullets
        self.reloudtimer = 0
        self.fire = False


    def update(self, delta_time, hull, player_in_sight):
        self.turret_update(delta_time, hull, player_in_sight)
        self.tank_shooting(delta_time)

    def turret_update(self, delta_time, hull, player_in_sight):
        Hx, Hy = hull.position
        if player_in_sight:
            Px, Py = self.player.position
            atan = math.atan2(-Px + Hx, -Py + Hy)
            if atan < 0:
                atan += 2 * math.pi
            angle_to_player = (math.degrees(atan)) % 360
        else:
            angle_to_player = hull.angle
        if abs(self.angle - angle_to_player) % 360 <\
                5 and player_in_sight:
            self.fire = True
            print('fire')
        else:
            self.fire = False

        if 0 < abs((angle_to_player - self.angle + 360) % 360) < 180:
            self.angle += TURRETROTATIONSPEED * delta_time
        if 360 > abs((angle_to_player - self.angle + 360) % 360) > 180:
            self.angle -= TURRETROTATIONSPEED * delta_time

        Tx = Hx - (10) * SCALE * math.sin(
            math.radians((self.angle) % 360))
        Ty = Hy - (10) * SCALE * math.cos(
            math.radians((self.angle) % 360))
        self.position = Tx, Ty

    def tank_shooting(self, delta_time):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if self.fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.1)
            self.reloudtimer = RELOUDTIME
            x, y = self.center_x, self.center_y
            angle = self.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle)),
                      y + -SCALE * 10 * math.cos(math.radians(angle)))
            newBullet = Bullet(self.bullet_path, Bx, By, angle, self.bullets)
            self.bullets.append(newBullet)


class Enemy(arcade.SpriteList):
    def __init__(self, player, bullets, walls):
        super().__init__()
        self.player = player
        self.bullets = bullets
        self.walls = walls
        self.hull = Tank_hull(player)
        self.turret = Tank_turret(player, bullets)
        self.append(self.hull)
        self.append(self.turret)

    def update(self, delta_time, enemies, explosions):
        self.player_in_sight = arcade.has_line_of_sight(
            self.player.position,
            self.hull.position,
            self.walls, ENEMY_VIEW,
            10)
        self.hull.update(delta_time, self.player_in_sight)
        self.turret.update(delta_time, self.hull,
                           self.player_in_sight)
        if self.hull.lives == 0:
            explosions.append(Explosion(*self.hull.position, explosions))
            enemies.remove(self)
