import arcade
from arcade.gui import (
    UITextureButton, UIManager, UIAnchorLayout, UIBoxLayout, UILabel)

# это должно быть в key_press в GameView
"""if key == arcade.key.ESCAPE:
    pause_view = PauseView(self)  # Передаём текущий вид, чтобы вернуться
    self.window.show_view(pause_view)
"""


class PauseView(arcade.View):
    def __init__(self, game_view, menu):
        super().__init__()
        self.game_view = game_view
        self.menu = menu
        self.manager = UIManager()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)

    def on_show_view(self):
        self.manager.enable()

        self.background_color = arcade.color.BLACK

    def on_hide_view(self):
        self.manager.disable()

    def setup_widgets(self):
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

        label = UILabel(text="ПАУЗА",
                        font_size=60,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        continue_game_button = UITextureButton(text='Продолжить игру',
                                               texture=texture_normal,
                                               texture_hovered=texture_hovered,
                                               texture_pressed=texture_pressed,
                                               scale=1.0)
        continue_game_button.on_click = self.continue_game_click
        self.box_layout.add(continue_game_button)

        main_menu_button = UITextureButton(text='Выйти в главное меню',
                                           texture=texture_normal,
                                           texture_hovered=texture_hovered,
                                           texture_pressed=texture_pressed,
                                           scale=1.0)
        main_menu_button.on_click = self.main_menu_button_click
        self.box_layout.add(main_menu_button)

    def on_draw(self):
        self.game_view.on_draw()

        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.game_view.forward = True
        if key == arcade.key.S:
            self.game_view.backward = True
        if key == arcade.key.A:
            self.game_view.left = True
        if key == arcade.key.D:
            self.game_view.right = True
        if key == arcade.key.ESCAPE:
            self.continue_game_click(None)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.game_view.forward = False
        if key == arcade.key.S:
            self.game_view.backward = False
        if key == arcade.key.A:
            self.game_view.left = False
        if key == arcade.key.D:
            self.game_view.right = False

    def continue_game_click(self, event):
        self.window.show_view(self.game_view)

    def main_menu_button_click(self, event):
        self.window.show_view(self.menu)


class MyGUIWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
