import arcade
from config import (SCALE, BULLET_TIME, BULLET_SPEED, 
                    BRAKINGFORCE, MAX_SPEED, ACCELERATION,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, RELOUDTIME)
import math
from bullet_class import Bullet


class Tank_hull(arcade.Sprite):
    def __init__(self, game_view):
        super().__init__(center_x=465, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_hull.png')
        self.game_view = game_view
        self.acceleration = 0
        self.speed = 0
        self.lives = 3

    def update(self, delta_time):
        self.tank_control(delta_time)

    def tank_control(self, delta_time):
        if self.game_view.forward or self.game_view.backward:
            if self.game_view.forward and not self.game_view.backward:
                if self.speed < 0:
                    self.acceleration = BRAKINGFORCE + ACCELERATION
                    self.speed = min(
                        (self.speed +
                         self.acceleration * delta_time, 0))
                else:
                    self.acceleration = ACCELERATION * (
                        (MAX_SPEED - abs(self.speed)) / MAX_SPEED)
                    self.speed += self.acceleration * delta_time
            if not self.game_view.forward and self.game_view.backward:
                if self.speed > 0:
                    self.acceleration = -(BRAKINGFORCE + ACCELERATION)
                    self.speed = max(
                        (self.speed +
                         self.acceleration * delta_time, 0))
                else:
                    self.acceleration = -ACCELERATION * (
                        (MAX_SPEED / 2 - abs(self.speed)) / MAX_SPEED)
                    self.speed += self.acceleration * delta_time

        if not self.game_view.backward and not self.game_view.forward:
            if self.speed > 0:
                self.acceleration = -BRAKINGFORCE
                self.speed = max(
                    (self.speed + self.acceleration * delta_time, 0))
            if self.speed < 0:
                self.acceleration = BRAKINGFORCE
                self.speed = min(
                    (self.speed + self.acceleration * delta_time, 0))
        
        turret_angle = self.game_view.tank_turret.angle

        if self.game_view.right and not self.game_view.left:
            if self.speed < 0:
                self.angle = self.angle - HULLROTATIONSPEED * delta_time
                self.game_view.tank_turret.angle = turret_angle - HULLROTATIONSPEED * delta_time
            else:
                self.angle = self.angle + HULLROTATIONSPEED * delta_time
                self.game_view.tank_turret.angle = turret_angle + HULLROTATIONSPEED * delta_time
        if not self.game_view.right and self.game_view.left:
            if self.speed < 0:
                self.angle = self.angle + HULLROTATIONSPEED * delta_time
                self.game_view.tank_turret.angle = turret_angle + HULLROTATIONSPEED * delta_time
            else:
                self.angle = self.angle - HULLROTATIONSPEED * delta_time
                self.game_view.tank_turret.angle = turret_angle - HULLROTATIONSPEED * delta_time

        speedx = self.speed * math.sin(
            math.radians(self.angle + 270)) * delta_time
        speedy = self.speed * math.cos(
            math.radians(self.angle + 270)) * delta_time

        self.position = (self.center_x + speedx, self.center_y + speedy)


class Tank_turret(arcade.Sprite):
    def __init__(self, game_view):
        super().__init__(center_x=465 - 16 * 4, center_y=465, scale=SCALE)
        self.texture = arcade.load_texture('assets/sprites/tank_turret.png')
        self.shoot_sound = arcade.load_sound("assets/sounds/shoot.mp3")
        self.game_view = game_view
        self.reloudtimer = 0

    def update(self, delta_time):
        self.turret_update(delta_time)
        self.tank_shooting(delta_time)

    def turret_update(self, delta_time):
        Wx, Wy = self.game_view.width // 2, self.game_view.height // 2
        Mx, My = self.game_view.mouseXY
        Hx, Hy = self.game_view.tank_hull.position
        atan = -math.atan2(Wy - My, Wx - Mx)
        if atan < 0:
            atan += 2 * math.pi
        mouse_angle = math.degrees(atan)
        if 0 < abs((mouse_angle - self.angle + 360) % 360) < 180:
            self.angle += TURRETROTATIONSPEED * delta_time
        if 360 > abs((mouse_angle - self.angle + 360) % 360) > 180:
            self.angle -= TURRETROTATIONSPEED * delta_time

        Tx = Hx - (-11 + 26) * SCALE * math.sin(
            math.radians((self.angle + 90) % 360))
        Ty = Hy - (-11 + 26) * SCALE * math.cos(
            math.radians((self.angle + 90) % 360))
        self.position = Tx, Ty

    def tank_shooting(self, delta_time):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if self.game_view.fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.5)
            self.reloudtimer = RELOUDTIME
            x, y = self.center_x, self.center_y
            angle = self.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle + 90)),
                      y + -SCALE * 10 * math.cos(math.radians(angle + 90)))
            newBullet = Bullet(Bx, By, angle, self.game_view.bullets)
            self.game_view.bullets.append(newBullet)

