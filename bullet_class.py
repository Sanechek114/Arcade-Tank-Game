import arcade
import math
from config import SCALE, BULLET_SPEED, BULLET_TIME


class Bullet(arcade.Sprite):
    def __init__(self, path, center_x, center_y, angle, speed_coef, damage, bul_list, player=False):
        super().__init__(
            path, SCALE, center_x, center_y, angle)
        self.bullet_timer = 0
        self.player = player
        self.damage = damage
        self.change_x, self.change_y = (
            BULLET_SPEED * speed_coef * math.sin(math.radians(angle)),
            BULLET_SPEED * speed_coef * math.cos(math.radians(angle)))
        self.bul_list = bul_list

    def update(self, delta_time):
        self.bullet_timer += delta_time
        if self.bullet_timer > BULLET_TIME:
            self.bul_list.remove(self)
        self.position = (self.center_x + self.change_x * delta_time,
                         self.center_y + self.change_y * delta_time)
