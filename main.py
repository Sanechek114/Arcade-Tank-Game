import arcade
import random
from pyglet.graphics import Batch
import math

SCALE = 4


class Tank_hull(arcade.Sprite):
    def __init__(self):
        super().__init__(center_x=465, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_hull.png')


class Tank_turret(arcade.Sprite):
    def __init__(self):
        super().__init__(center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_turret.png')


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tile_map = arcade.load_tilemap("assets/map1.tmx", SCALE)
        self.scene = self.tile_map.sprite_lists['grass']
        for block in self.scene:
            r = random.choice([block.texture.rotate_90(), block.texture.rotate_180(), block.texture.rotate_270(), block.texture])
            block.texture = r
            fh = random.choice([block.texture.flip_horizontally(), block.texture])
            block.texture = fh
            fv = random.choice([block.texture.flip_vertically(), block.texture])
            block.texture = fv
        self.reloudtimer = 0
        self.mouseXY = (0, 0)

        self.tank_hull = Tank_hull()
        self.tank_turret = Tank_turret()

        self.tank = arcade.SpriteList()
        self.tank.append(self.tank_hull)
        self.tank.append(self.tank_turret)

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)
        self.tank.draw(pixelated=True)

    def on_update(self, delta_time):
        self.reloudtimer = max(self.reloudtimer - 1 * delta_time, 0)

        Tx, Ty = self.tank_turret.position
        Mx, My = self.mouseXY
        Hx, Hy = self.tank_hull.position
        atan = -math.atan2(Hy - My, Hx - Mx)
        if atan < 0:
            atan += 2 * math.pi
        turret_angle = math.degrees(atan)
        self.tank_turret.angle = turret_angle
        Tx = Hx - (-11 + 26) * SCALE * math.sin(math.radians((turret_angle + 90) % 360))
        Ty = Hy - (-11 + 26) * SCALE * math.cos(math.radians((turret_angle + 90) % 360))
        self.tank_turret.position = Tx, Ty

    def on_key_press(self, key, modifiers):
        self.forward = key == arcade.key.W
        self.backward = key == arcade.key.S
        self.right = key == arcade.key.A
        self.left = key == arcade.key.D
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouseXY = (x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.reloudtimer == 0:
            self.fire = True
            self.reloudtimer = RELOUDTIME


window = arcade.Window(960, 960, 'игра про танки')
menu_view = GameView()
window.show_view(menu_view)
arcade.run()