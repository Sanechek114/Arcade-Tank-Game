import arcade
from config import SCALE, ANIMATION_SPEED


class Explosion(arcade.Sprite):
    def __init__(self, x, y, exp_list):
        super().__init__(center_x=x, center_y=y, scale=SCALE)
        for n in range(5):
            self.textures.append(arcade.load_texture(f"assets/sprites/hit/explosionSmoke{n + 1}.png"))
        print(len(self.textures))
        self.texture = self.textures[0]
        self.texture_timer = 0
        self.texture_id = 1
        self.exp_list = exp_list

    def update(self, delta_time):
        self.texture_timer += delta_time
        if self.texture_timer > ANIMATION_SPEED:
            self.texture_timer = 0
            self.texture_id = (self.texture_id + 1) % 5
            self.texture = self.textures[self.texture_id]
        if self.texture_id == 0:
            self.exp_list.remove(self)
