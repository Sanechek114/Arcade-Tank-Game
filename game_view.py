import arcade
import random
from config import (SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, RELOUDTIME,
                    CAMERA_LERP)
from tank import Tank_hull, Tank_turret
from explosion import Explosion


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.world_camera = arcade.camera.Camera2D()
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT
        # карта
        self.tile_map = arcade.load_tilemap("assets/map1.tmx", SCALE)
        self.scene = self.tile_map.sprite_lists['grass']
        for block in self.scene:
            r = random.choice([block.texture.rotate_90(),
                               block.texture.rotate_180(),
                               block.texture.rotate_270(), block.texture])
            block.texture = r
            fh = random.choice([block.texture.flip_horizontally(),
                                block.texture])
            block.texture = fh
            fv = random.choice([block.texture.flip_vertically(),
                                block.texture])
            block.texture = fv

        self.reloudtimer = 0
        self.mouseXY = (0, 0)
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.fire = False

        self.tank_hull = Tank_hull(self)
        self.tank_turret = Tank_turret(self)

        self.tank = arcade.SpriteList()
        self.tank.append(self.tank_hull)
        self.tank.append(self.tank_turret)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.scene.draw(pixelated=True)
        self.bullets.draw(pixelated=True)
        self.tank.draw(pixelated=True)
        self.explosions.draw(pixelated=True)
        self.draw_reloding()

    def on_update(self, delta_time):
        self.tank_hull.update(delta_time)
        self.tank_turret.update(delta_time)
        self.bullets.update(delta_time)
        self.explosions.update(delta_time)
        self.world_camera_update()

    def draw_reloding(self):
        try:
            dx = (RELOUDTIME - self.tank_turret.reloudtimer) / RELOUDTIME
        except ZeroDivisionError:
            dx = 0
        x, y = self.world_camera.position
        arcade.draw_lbwh_rectangle_filled(
            x - self.width * 0.15, y - self.height * 0.45,
            self.width * 0.3 * dx, SCALE * 4, arcade.color.GREEN)
        arcade.draw_lbwh_rectangle_filled(
            x + self.width * 0.15, y - self.height * 0.45,
            -self.width * 0.3 * (1 - dx), SCALE * 4, arcade.color.RED)

    def world_camera_update(self):
        position = (
            self.tank_hull.center_x,
            self.tank_hull.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP,
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.forward = True
        if key == arcade.key.S:
            self.backward = True
        if key == arcade.key.A:
            self.left = True
        if key == arcade.key.D:
            self.right = True
        if key == arcade.key.J:
            x, y = 0, 0
            self.explosions.append(Explosion(x, y, self.explosions))

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.forward = False
        if key == arcade.key.S:
            self.backward = False
        if key == arcade.key.A:
            self.left = False
        if key == arcade.key.D:
            self.right = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouseXY = (x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire = False
