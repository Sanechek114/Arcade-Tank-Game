import arcade
import math
from config import SCALE, BULLET_SPEED, BULLET_TIME


class Bullet(arcade.Sprite):
    def __init__(self, center_x, center_y, angle, bul_list, player=False):
        super().__init__(
            'assets/sprites/bullet.png', SCALE, center_x, center_y, angle)
        self.texture = self.texture.flip_horizontally()
        self.bullet_timer = 0
        self.player = player
        self.change_x, self.change_y = (
            BULLET_SPEED * math.sin(math.radians(angle - 90 + 360)),
            BULLET_SPEED * math.cos(math.radians(angle - 90)))
        self.bul_list = bul_list

    def update(self, delta_time):
        self.bullet_timer += delta_time
        if self.bullet_timer > BULLET_TIME:
            self.bul_list.remove(self)
        self.position = (self.center_x + self.change_x * delta_time,
                         self.center_y + self.change_y * delta_time)
