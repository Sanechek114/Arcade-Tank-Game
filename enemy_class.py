import arcade
from config import (SCALE, ENEMY_VIEW, MAX_SPEED, BULLET_SPEED,
                    HULLROTATIONSPEED, TURRETROTATIONSPEED, RELOUDTIME)
from bullet_class import Bullet
import math
from explosion import Explosion


class Tank_hull(arcade.Sprite):
    def __init__(self, path, player, lives):
        super().__init__(path, SCALE, 465, 465)
        self.player = player
        self.speed = MAX_SPEED / 3
        self.on_point = True
        self.player_point = self.position
        self.target_angle = self.angle
        self.lives = lives

    def next_point(self, player_in_sight):
        Hx, Hy = self.position
        if player_in_sight:
            self.player_point = self.player.position
        atan = math.atan2((-self.player_point[0] + Hx),
                          (-self.player_point[1] + Hy))
        self.target_angle = math.degrees(atan) % 360
        self.on_point = math.sqrt(
            (self.player_point[0] - Hx) ** 2 + \
            (self.player_point[1] - Hy) ** 2) < 100 * SCALE

    def update(self, delta_time, player_in_sight):
        self.next_point(player_in_sight)
        self.enemy_rotate(delta_time)
        if abs(self.target_angle - self.angle) % 360 <= 60:
            self.position = (self.center_x + self.change_x,
                             self.center_y + self.change_y)

    def enemy_rotate(self, delta_time):
        if 0 < abs((self.target_angle - self.angle + 360) % 360) < 180:
            self.angle += HULLROTATIONSPEED / 1.5 * delta_time
        if 360 > abs((self.target_angle - self.angle + 360) % 360) > 180:
            self.angle -= HULLROTATIONSPEED / 1.5 * delta_time
        if not self.on_point:
            self.change_x = self.speed * math.sin(
                math.radians(self.angle + 180)) * delta_time
            self.change_y = self.speed * math.cos(
                math.radians(self.angle + 180)) * delta_time
        else:
            self.change_x, self.change_y = 0, 0


class Tank_turret(arcade.Sprite):
    def __init__(self, path, bullet_path, player, bullets, bullet_speed_coef, bullet_damage):
        super().__init__(path, center_x=200, center_y=800, scale=SCALE)
        self.shoot_sound = arcade.load_sound("assets/sounds/awp.mp3")
        self.reloudtime = RELOUDTIME
        self.bullet_path = bullet_path
        self.bullet_speed_coef = bullet_speed_coef
        self.bullet_damage = bullet_damage
        self.player = player
        self.bullets = bullets
        self.reloudtimer = 0
        self.fire = False

    def update(self, delta_time, hull, player_in_sight):
        self.turret_update(delta_time, hull, player_in_sight)
        self.tank_shooting(delta_time)

    def turret_update(self, delta_time, hull, player_in_sight):
        Hx, Hy = hull.position
        if player_in_sight:
            Px, Py = self.player.position
            time = arcade.get_distance_between_sprites(self.player, hull) / (
                self.bullet_speed_coef * BULLET_SPEED)
            Px, Py = Px + self.player.change_x * time * 100, Py + self.player.change_y * time * 100
            atan = math.atan2(-Px + Hx, -Py + Hy)
            if atan < 0:
                atan += 2 * math.pi
            angle_to_player = (math.degrees(atan)) % 360
        else:
            angle_to_player = hull.angle
        if abs(self.angle - angle_to_player) % 360 <\
                5 and player_in_sight:
            self.fire = True
        else:
            self.fire = False

        if 0 < abs((angle_to_player - self.angle + 360) % 360) < 180:
            self.angle += TURRETROTATIONSPEED * delta_time
        if 360 > abs((angle_to_player - self.angle + 360) % 360) > 180:
            self.angle -= TURRETROTATIONSPEED * delta_time
        # Выравнивание пушки
        Tx = Hx - (10) * SCALE * math.sin(
            math.radians((self.angle) % 360))
        Ty = Hy - (10) * SCALE * math.cos(
            math.radians((self.angle) % 360))

        self.position = Tx, Ty

    def tank_shooting(self, delta_time):
        self.reloudtimer = max(self.reloudtimer - delta_time, 0)
        if self.fire and self.reloudtimer == 0:
            self.shoot_sound.play(0.1)
            self.reloudtimer = self.reloudtime
            x, y = self.center_x, self.center_y
            angle = self.angle
            Bx, By = (x + -SCALE * 10 * math.sin(math.radians(angle)),
                      y + -SCALE * 10 * math.cos(math.radians(angle)))
            newBullet = Bullet(self.bullet_path, Bx, By, angle - 180,
                               self.bullet_speed_coef, self.bullet_damage,
                               self.bullets)
            self.bullets.append(newBullet)


class Enemy(arcade.SpriteList):
    def __init__(self, enemy_id,  player, bullets):
        super().__init__()
        self.player = player
        self.bullets = bullets
        # id: (lives, damage, bullet speed coef)
        enemy_lives, bullet_damage, bullet_speed, = {
            1: (2, 1, 1.25),
            2: (3, 2, 0.1),
            3: (6, 2, 1.25)}[enemy_id]


        self.turret_path = f"assets/sprites/barrels/enemy/specialBarrel{enemy_id}.png"
        self.hull_path = f"assets/sprites/bodyes/enemy/tankBody_{enemy_id}.png"
        self.bullet_path = f"assets/sprites/bullets/enemy/bulletDark{enemy_id}_outline.png"
        self.hull = Tank_hull(self.hull_path, player, enemy_lives)
        self.turret = Tank_turret(self.turret_path, self.bullet_path,
                                  player, bullets, bullet_speed, bullet_damage)

        self.append(self.hull)
        self.append(self.turret)

    def update(self, delta_time, enemies, enemies_hulls, explosions, walls):
        self.player_in_sight = arcade.has_line_of_sight(
            self.player.position,
            self.hull.position,
            walls, ENEMY_VIEW,
            10)
        self.hull.update(delta_time, self.player_in_sight)
        self.turret.update(delta_time, self.hull,
                           self.player_in_sight)
        if self.hull.lives <= 0:
            explosions.append(Explosion(*self.hull.position, explosions))
            enemies.remove(self)
            enemies_hulls.remove(self.hull)


class Boss(arcade.SpriteList):
    def __init__(self, player, bullets):
        super().__init__()
        self.player = player
        self.bullets = bullets
        lives = 16

        bullet_speed1 = 1.5
        bullet_damage1 = 2
        bullet_speed2 = 1
        bullet_damage2 = 4

        self.turret_path1 = "assets/sprites/barrels/enemy/specialBarrel2.png"
        self.turret_path2 = "assets/sprites/barrels/enemy/specialBarrel3.png"
        self.hull_path = "assets/sprites/bodyes/enemy/tankBody_4.png"
        self.bullet_path1 = "assets/sprites/bullets/enemy/bulletDark3_outline.png"
        self.bullet_path2 = "assets/sprites/bullets/enemy/bulletDark2_outline.png"
        self.hull = Tank_hull(self.hull_path, player, lives)
        self.turret1 = Tank_turret(self.turret_path1, self.bullet_path1,
                                   player, bullets, bullet_speed1, bullet_damage1)
        self.turret1.reloudtime = RELOUDTIME * 1.5
        self.turret2 = Tank_turret(self.turret_path2, self.bullet_path2,
                                   player, bullets, bullet_speed2, bullet_damage2)

        self.append(self.hull)
        self.append(self.turret1)
        self.append(self.turret2)

    def update(self, delta_time, enemies, enemies_hulls, explosions, walls):
        self.player_in_sight = arcade.has_line_of_sight(
            self.player.position,
            self.hull.position,
            walls, ENEMY_VIEW * 3,
            1)
        self.hull.update(delta_time, self.player_in_sight)
        self.turret1.update(delta_time, self.hull,
                            self.player_in_sight)
        self.turret2.update(delta_time, self.hull,
                            self.player_in_sight)
        angle = self.hull.angle
        x, y = self.turret1.position
        dx, dy = SCALE * 16 * math.sin(math.radians(angle)), SCALE * 16 * math.cos(math.radians(angle))
        self.turret1.position = x + dx, y + dy
        self.turret2.position = x - dx, y - dy
        
        if self.hull.lives <= 0:
            explosions.append(Explosion(*self.hull.position, explosions))
            enemies.remove(self)
            enemies_hulls.remove(self.hull)

