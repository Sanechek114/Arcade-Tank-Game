import arcade

num_file = int(input('КАКУЮ КАРТУ ПОКАЗАТЬ? 1, 2 или 3: '))
tmx = f"assets/tank_map_{num_file}.tmx"


class MapViewer(arcade.Window):
    def __init__(self):
        super().__init__(fullscreen=True, title="tank_map_1")


        self.tile_map = None
        self.scene = None

    def setup(self):

        temp_map = arcade.load_tilemap(tmx, scaling=1.0)
        px = temp_map.width * temp_map.tile_width
        auto_scaling = self.width / px

        self.tile_map = arcade.load_tilemap(tmx, scaling=auto_scaling)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()


if __name__ == "__main__":
    window = MapViewer()
    window.setup()
    arcade.run()
