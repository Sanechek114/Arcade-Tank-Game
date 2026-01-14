import arcade
from config import (SCALE, ENEMY_VIEW, MAX_SPEED,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, RELOUDTIME)
from bullet_class import Bullet
import math


class Tank_hull(arcade.Sprite):
    def __init__(self, game_view, route):
        super().__init__(scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_hull.png')
        self.route = route
        self.point_id = 0
        self.point = self.route[self.point_id]
        self.position = self.point
        self.in_moving = True
        self.game_view = game_view
        self.speed = MAX_SPEED / 3
        self.next_point()

    def next_point(self):
        self.in_moving = False
        self.point_id = (self.point_id + 1 + len(self.route)) % len(self.route)
        self.point = self.route[self.point_id]
        Px, Py = self.point
        Hx, Hy = self.position
        atan = -math.atan2(Py - Hy, Px - Hx)
        if atan < 0:
            atan += 2 * math.pi
        self.target_angle = math.degrees(atan) + 180

    def update(self, delta_time):
        if abs(self.position[0] - self.point[0]) < 2 and abs(
                self.position[1] - self.point[1]) < 2:
            self.next_point()
        if self.in_moving:
            self.position = (self.center_x + self.change_x,
                             self.center_y + self.change_y)
        else:
            self.enemy_rotate(delta_time)

    def enemy_rotate(self, delta_time):
        if 0 < abs((self.target_angle - self.angle + 360) % 360) < 180:
            self.angle += HULLROTATIONSPEED * delta_time
        if 360 > abs((self.target_angle - self.angle + 360) % 360) > 180:
            self.angle -= HULLROTATIONSPEED * delta_time
        if abs(self.angle - self.target_angle) % 360 < 1:
            print('stop rot')
            self.angle = self.target_angle
            self.in_moving = True
            self.change_x = self.speed * math.sin(
                math.radians(self.angle + 270)) * delta_time
            self.change_y = self.speed * math.cos(
                math.radians(self.angle + 270)) * delta_time


class Tank_turret(arcade.Sprite):
    def __init__(self, game_view):
        super().__init__(center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_turret.png')
        self.shoot_sound = arcade.load_sound("assets/sounds/awp.mp3")
        self.game_view = game_view
        self.reloudtimer = 0
        self.player_in_sight = True
        self.fire = False

    def update(self, delta_time, hull):
        self.turret_update(delta_time, hull)
        self.tank_shooting(delta_time)

    def turret_update(self, delta_time, hull):
        Hx, Hy = hull.position
        if self.player_in_sight:
            Px, Py = self.game_view.tank_hull.position
            atan = -math.atan2(Py - Hy, Px - Hx)
            if atan < 0:
                atan += 2 * math.pi
            angle_to_player = math.degrees(atan) + 180
        else:
            angle_to_player = hull.angle
        if abs(self.angle - angle_to_player) % 360 <\
                5 and self.player_in_sight:
            self.fire = True
            print('fire')
        else:
            self.fire = False

        if 0 < abs((angle_to_player - self.angle + 360) % 360) < 180:
            self.angle += TURRETROTATIONSPEED * delta_time
        if 360 > abs((angle_to_player - self.angle + 360) % 360) > 180:
            self.angle -= TURRETROTATIONSPEED * delta_time

        Tx = Hx - (-11 + 26) * SCALE * math.sin(
            math.radians((self.angle + 90) % 360))
        Ty = Hy - (-11 + 26) * SCALE * math.cos(
            math.radians((self.angle + 90) % 360))
        self.position = Tx, Ty

    def tank_shooting(self, delta_time):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if self.fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.5)
            self.reloudtimer = RELOUDTIME
            x, y = self.center_x, self.center_y
            angle = self.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle + 90)),
                      y + -SCALE * 10 * math.cos(math.radians(angle + 90)))
            newBullet = Bullet(Bx, By, angle, self.game_view.bullets)
            self.game_view.bullets.append(newBullet)


class Enemy(arcade.SpriteList):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.route = [(304, 105), (505, 308), (103, 203)]
        self.hull = Tank_hull(self.game_view, self.route)
        self.turret = Tank_turret(self.game_view)
        self.append(self.hull)
        self.append(self.turret)
        self.lives = 2

    def update(self, delta_time):
        self.turret.player_in_sight = arcade.has_line_of_sight(
            self.game_view.tank_hull.position,
            self.hull.position,
            self.game_view.explosions, ENEMY_VIEW)
        self.hull.update(delta_time)
        self.turret.update(delta_time, self.hull)

        
arcade.DefaultTextureAtlas