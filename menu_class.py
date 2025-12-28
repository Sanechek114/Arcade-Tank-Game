import arcade
from arcade.gui import UITextureButton, UIManager, UIAnchorLayout, UIBoxLayout

from pyglet.graphics import Batch


# from main import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        # self.setup_widgets()

        self.anchor_layout.add(self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)

        self.batch = Batch()
        self.main_text = arcade.Text("Arcade Tank", self.window.width / 2, self.window.height / 2 + 100,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        # self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 150,
        #                             arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()
        # self.manager.draw()


window = arcade.Window(800, 600, "")
menu_view = MenuView()
window.show_view(menu_view)
arcade.run()
