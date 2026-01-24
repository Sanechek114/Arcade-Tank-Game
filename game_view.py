import arcade
from random import randint, choice
from config import (SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, RELOUDTIME,
                    CAMERA_LERP)
from tank import Player
from explosion import Explosion
from pause_class import PauseView
from enemy_class import Enemy, Boss
from menu_game_over import GameOverView
from menu_win import WinView
import time


class GameView(arcade.View):
    def __init__(self, menu, color, turret, map):
        super().__init__()
        self.menu = menu
        self.background_color = (57, 194, 114)
        self.world_camera = arcade.camera.Camera2D()
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT
        # карта
        self.tile_map = arcade.load_tilemap(
            f"assets/tank_map_{map}.tmx", SCALE, use_spatial_hash=True)
        self.scene = self.tile_map.sprite_lists['grass']
        self.static = self.tile_map.sprite_lists['statics']
        self.trees = self.tile_map.sprite_lists['trees']
        self.breaking = self.tile_map.sprite_lists['breaking']
        self.decorations = self.tile_map.sprite_lists['decorations']

        self.ai_walls = arcade.SpriteList(True)
        self.ai_walls.extend(self.static)
        self.ai_walls.extend(self.trees)
        self.ai_walls.extend(self.breaking)

        self.reloudtimer = 0
        self.mouseXY = (0, 0)
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.fire = False

        self.game_over = False

        self.walls = arcade.SpriteList(True)
        self.walls.extend(self.static)
        self.walls.extend(self.breaking)

        self.player = Player(color, turret, self.bullets, self.explosions, self.walls)

        self.enemy = Enemy(1, self.player.hull, self.bullets)
        self.enemy.collision = arcade.PhysicsEngineSimple(
            self.enemy.hull, self.walls)
        self.enemies = []
        self.enemies.append(self.enemy)

        self.collision = arcade.PhysicsEngineSimple(
            self.player.hull, self.walls)

        self.enemies_hulls = arcade.SpriteList()
        self.enemies_hulls_collision = []
        for enemy in self.enemies:
            self.enemies_hulls.append(enemy.hull)

        self.enemy_to_player_colis = arcade.PhysicsEngineSimple(
            self.player.hull, self.enemies_hulls)

        time.sleep(1)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.scene.draw(pixelated=True)
        self.decorations.draw(pixelated=True)
        self.static.draw(pixelated=True)
        self.breaking.draw(pixelated=True)
        self.bullets.draw(pixelated=True)
        self.player.draw(pixelated=True)
        for enemy in self.enemies:
            enemy.draw(pixelated=True)
        self.trees.draw(pixelated=True)
        self.explosions.draw(pixelated=True)
        self.draw_reloding_lives()

    def on_update(self, delta_time):
        control = (self.forward, self.backward,
                   self.right, self.left, self.fire, self.mouseXY)

        if not self.game_over:
            self.player.update(delta_time, control)
            if self.player.lives <= 0:
                self.game_over = True
                self.player.hull.change_x = 0
                self.player.hull.change_y = 0
                self.player.hull.speed = 0
                arcade.schedule_once(self.open_game_over, 2)
        if len(self.enemies) == 0:
            arcade.schedule_once(self.open_game_win, 2)

        #  Обновление врагов
        trees = []
        for enemy in self.enemies:
            enemy.update(delta_time, self.enemies, self.enemies_hulls, self.explosions, self.ai_walls)
            enemy.collision.update()
            trees += (arcade.check_for_collision_with_list(enemy.hull, self.trees))  # Проверка коллизия ботов и деревьев

        trees += (arcade.check_for_collision_with_list(self.player.hull, self.trees))  # Проверка коллизия игрока и деревьев

        for tree in trees:
            x, y = tree.position
            for _ in range(3):
                tx, ty = x + randint(-30, 30) * SCALE, y + randint(-30, 30) * SCALE
                self.decorations.append(arcade.Sprite(
                    choice(['assets/objects/treeGreen_twigs.png',
                            'assets/objects/treeBrown_twigs.png']),
                    SCALE, tx, ty, randint(1, 360)))  # Спавн 3 веток рядом с разрушеным деревом
            self.trees.remove(tree)  # Удаление дерева
            self.ai_walls.remove(tree)

        colliding = self.enemy_to_player_colis.update()  # Обновление коллизии игрока и ботов
        colliding += self.collision.update()  # Обновление коллизии игрока и стен

        if len(colliding):
            self.player.hull.speed = 0  # Остоновка игрока при столкновениях

        self.bullets.update(delta_time)
        self.explosions.update(delta_time)
        self.world_camera_update()
        bullets = arcade.check_for_collision_with_list(
            self.player.hull, self.bullets)
        if bullets:
            for bullet in bullets:
                if not bullet.player:
                    self.player.lives -= bullet.damage
                    print(bullet.damage)
                    self.bullets.remove(bullet)
                    if self.player.lives <= 0:
                        self.explosions.append(
                            Explosion(*self.player.hull.position,
                                      self.explosions))
        for bullet in self.bullets:
            broken = arcade.check_for_collision_with_list(
                bullet, self.breaking, 3)
            static = arcade.check_for_collision_with_list(
                bullet, self.static, 3)
            enemies_hulls = arcade.check_for_collision_with_list(
                bullet, self.enemies_hulls, 3)

            if broken:
                self.bullets.remove(bullet)
                for elem in broken:
                    self.breaking.remove(elem)
                    self.ai_walls.remove(elem)
                    self.walls.remove(elem)

            elif enemies_hulls and bullet.player:
                print(bullet.damage)
                self.bullets.remove(bullet)
                for hull in enemies_hulls:
                    hull.next_point(True)
                    hull.lives -= bullet.damage

            elif static:
                self.bullets.remove(bullet)

    def draw_reloding_lives(self):
        lives, reloudtime, reloudtimer = self.player.get_lives_relouding()
        try:
            dx = (reloudtime - reloudtimer) / reloudtime
        except ZeroDivisionError:
            dx = 0
        x, y = self.world_camera.position
        arcade.draw_lbwh_rectangle_filled(
            x - self.width * 0.15, y - self.height * 0.45,
            self.width * 0.3 * dx, SCALE * 4, arcade.color.GREEN)
        arcade.draw_lbwh_rectangle_filled(
            x + self.width * 0.15, y - self.height * 0.45,
            -self.width * 0.3 * (1 - dx), SCALE * 4, arcade.color.RED)
        for n in range(lives):
            arcade.draw_lbwh_rectangle_filled(
                x - self.width * 0.14 + n * 0.1 * self.width,
                y - self.height * 0.43,
                self.width * 0.08, SCALE * 4, arcade.color.RED)

    def open_game_over(self, event):
        self.window.show_view(GameOverView(self, self.menu))

    def open_game_win(self, event):
        self.window.show_view(WinView(self, self.menu))

    def world_camera_update(self):
        position = (
            self.player.hull.center_x,
            self.player.hull.center_y
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
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self, self.menu)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.forward = False
        if key == arcade.key.S:
            self.backward = False
        if key == arcade.key.A:
            self.left = False
        if key == arcade.key.D:
            self.right = False
    
    def on_close(self):
        arcade.unschedule(self.open_game_over)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouseXY = (x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire = False
