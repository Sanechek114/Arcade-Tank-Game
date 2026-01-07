import arcade
from config import SCALE, ANIMATION_SPEED

class Explosion(arcade.Sprite):
    def __init__(self, x, y, exp_list):
        super().__init__(center_x=x, center_y=y, scale=SCALE, )
        spritesheet = arcade.SpriteSheet('assets/tiles/explosion.png')
        self.textures = spritesheet.get_texture_grid((100, 100), 9, 81)
        print(len(self.textures))
        self.texture = self.textures[0]
        self.texture_timer = 0
        self.texture_id = 1
        self.exp_list = exp_list

    def update(self, delta_time):
        self.texture_timer += delta_time
        if self.texture_timer > ANIMATION_SPEED:
            self.texture_timer = 0
            self.texture_id = (self.texture_id + 82) % 81
            self.texture = self.textures[self.texture_id]
        if self.texture_id == 73:
            self.exp_list.remove(self)
