import arcade
import random
from pyglet.graphics import Batch
import math
from config import (SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, RELOUDTIME,
                    BRAKINGFORCE, ACCELERATION, MAX_SPEED,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, CAMERA_LERP)
from tank import Tank_hull, Tank_turret, Bullet
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
            r = random.choice([block.texture.rotate_90(), block.texture.rotate_180(), block.texture.rotate_270(), block.texture])
            block.texture = r
            fh = random.choice([block.texture.flip_horizontally(), block.texture])
            block.texture = fh
            fv = random.choice([block.texture.flip_vertically(), block.texture])
            block.texture = fv

        self.reloudtimer = 0
        self.tank_acceleration = 0
        self.tank_speed = 0
        self.mouseXY = (0, 0)
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.fire = False

        self.shoot_sound = arcade.load_sound("assets/sounds/awp.mp3")

        self.tank_hull = Tank_hull()
        self.tank_turret = Tank_turret()

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
        self.tank_control(delta_time)
        self.turret_update(delta_time)
        self.tank_shooting(delta_time)
        self.bullets.update(delta_time)
        self.explosions.update(delta_time)
        self.world_camera_update()

    def tank_shooting(self, delta_time):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if self.fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.5)
            self.reloudtimer = RELOUDTIME
            x, y = self.tank_turret.center_x, self.tank_turret.center_y
            angle = self.tank_turret.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle + 90)),
                      y + -SCALE * 10 * math.cos(math.radians(angle + 90)))
            newBullet = Bullet(Bx, By, angle, self.bullets)
            self.bullets.append(newBullet)

    def draw_reloding(self):
        try:
            dx = (RELOUDTIME - self.reloudtimer) / RELOUDTIME
        except ZeroDivisionError:
            dx = 0
        x, y = self.world_camera.position
        arcade.draw_lbwh_rectangle_filled(x - self.width * 0.15, y - self.height * 0.45, self.width * 0.3 * dx, SCALE * 4, arcade.color.GREEN)
        arcade.draw_lbwh_rectangle_filled(x + self.width * 0.15, y - self.height * 0.45, -self.width * 0.3 * (1 - dx), SCALE * 4, arcade.color.RED)

    def tank_control(self, delta_time):
        if self.forward or self.backward:
            if self.forward and not self.backward:
                if self.tank_speed < 0:
                    self.tank_acceleration = BRAKINGFORCE
                    self.tank_speed = min(
                        (self.tank_speed +
                         self.tank_acceleration * delta_time, 0))
                else:
                    self.tank_acceleration = ACCELERATION * (
                        MAX_SPEED - abs(self.tank_speed)) * delta_time
            if not self.forward and self.backward:
                if self.tank_speed > 0:
                    self.tank_acceleration = -BRAKINGFORCE
                    self.tank_speed = max(
                        (self.tank_speed +
                         self.tank_acceleration * delta_time, 0))
                else:
                    self.tank_acceleration = -ACCELERATION * 0.5 * (
                        MAX_SPEED - abs(self.tank_speed)) * delta_time
            self.tank_speed += self.tank_acceleration * delta_time

        if not self.backward and not self.forward:
            if self.tank_speed > 0:
                self.tank_acceleration = -BRAKINGFORCE
                self.tank_speed = max((self.tank_speed +
                                       self.tank_acceleration * delta_time, 0))
            if self.tank_speed < 0:
                self.tank_acceleration = BRAKINGFORCE
                self.tank_speed = min((self.tank_speed + self.tank_acceleration * delta_time, 0))

        if self.right and not self.left:
            if self.tank_speed < 0:
                self.tank_hull.angle = self.tank_hull.angle - HULLROTATIONSPEED * delta_time
            else:
                self.tank_hull.angle = self.tank_hull.angle + HULLROTATIONSPEED * delta_time
        if not self.right and self.left:
            if self.tank_speed < 0:
                self.tank_hull.angle = self.tank_hull.angle + HULLROTATIONSPEED * delta_time
            else:
                self.tank_hull.angle = self.tank_hull.angle - HULLROTATIONSPEED * delta_time

        speedx = self.tank_speed * math.sin(math.radians(self.tank_hull.angle + 270)) * delta_time
        speedy = self.tank_speed * math.cos(math.radians(self.tank_hull.angle + 270)) * delta_time

        self.tank_hull.position = (self.tank_hull.center_x + speedx, self.tank_hull.center_y + speedy)

    def turret_update(self, delta_time):
        Wx, Wy = self.width // 2, self.height // 2
        Mx, My = self.mouseXY
        Hx, Hy = self.tank_hull.position
        atan = -math.atan2(Wy - My, Wx - Mx)
        if atan < 0:
            atan += 2 * math.pi
        mouse_angle = math.degrees(atan)
        if 0 < abs((mouse_angle - self.tank_turret.angle + 360) % 360) < 180:
            self.tank_turret.angle += TURRETROTATIONSPEED * delta_time
        if 360 > abs((mouse_angle - self.tank_turret.angle + 360) % 360) > 180:
            self.tank_turret.angle -= TURRETROTATIONSPEED * delta_time

        Tx = Hx - (-11 + 26) * SCALE * math.sin(math.radians((self.tank_turret.angle + 90) % 360))
        Ty = Hy - (-11 + 26) * SCALE * math.cos(math.radians((self.tank_turret.angle + 90) % 360))
        self.tank_turret.position = Tx, Ty

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
            x, y = self.tank_hull.position
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
