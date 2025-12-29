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
        self.game_view = game_view  # Сохраняем, чтобы вернуться
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", self.window.width / 2, self.window.height / 2,
                                      arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)


    def setup_widgets(self):
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

        # если нажать заработает метод start_game_click
        start_game_button = UITextureButton(text='Начать игру',
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=1.0,
                                            )
        start_game_button.on_click = self.start_game_click
        self.box_layout.add(start_game_button)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(self.game_view)  # Возвращаемся в игру

    def start_game_click(self):
        pass