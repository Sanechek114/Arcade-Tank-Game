import arcade
from arcade.gui import UITextureButton, UIManager, UIAnchorLayout, UIBoxLayout
from pyglet.graphics import Batch

# это должно быть в key_press в GameView
"""if key == arcade.key.ESCAPE:
    pause_view = PauseView(self)  # Передаём текущий вид, чтобы вернуться
    self.window.show_view(pause_view)
"""


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = UIManager()

        self.batch = Batch()
        self.pause_text = arcade.Text("ПАУЗА", self.window.width / 2, self.window.height / 2 + 100,
                                      arcade.color.WHITE, font_size=60, anchor_x="center", batch=self.batch)

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)

    def on_show_view(self):
        self.manager.enable()

        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        self.manager.disable()

    def setup_widgets(self):
        """ Добавляет кнопки в меню паузы. """
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

        continue_game_button = UITextureButton(text='Продолжить игру',
                                               texture=texture_normal,
                                               texture_hovered=texture_hovered,
                                               texture_pressed=texture_pressed,
                                               scale=1.0)
        continue_game_button.on_click = self.on_continue_game_click
        self.box_layout.add(continue_game_button)

    def on_draw(self):
        self.game_view.on_draw()

        self.batch.draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.on_continue_game_click(None)

    def on_continue_game_click(self, event):
        self.window.show_view(self.game_view)


class MyGUIWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
