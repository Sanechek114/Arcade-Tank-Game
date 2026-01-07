import arcade
from config import SCALE, BULLET_TIME, BULLET_SPEED
import math


class Tank_hull(arcade.Sprite):
    def __init__(self):
        super().__init__(center_x=465, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_hull.png')


class Tank_turret(arcade.Sprite):
    def __init__(self):
        super().__init__(center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_turret.png')


class Bullet(arcade.Sprite):
    def __init__(self, center_x, center_y, angle, bul_list):
        super().__init__(
            'assets/sprites/bullet.png', SCALE, center_x, center_y, angle)
        self.texture = self.texture.flip_horizontally()
        self.livetime = 0
        self.change_x, self.change_y = (
            BULLET_SPEED * math.sin(math.radians(angle - 90 + 360)),
            BULLET_SPEED * math.cos(math.radians(angle - 90)))
        self.bul_list = bul_list

    def on_update(self, delta_time):
        self.bullet_timer += delta_time
        if self.bullet_timer > BULLET_TIME:
            self.bul_list.remove(self)
