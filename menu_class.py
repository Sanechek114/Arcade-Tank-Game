import arcade
from arcade.gui import (UITextureButton, UIManager, UIAnchorLayout, UIBoxLayout, UILabel)
from game_view import GameView


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)

        # self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 150,
        #                             arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def setup_widgets(self):
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

        label = UILabel(text="Танчики",
                        font_size=60,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        # если нажать заработает метод start_game_click
        start_game_button = UITextureButton(text='Начать игру',
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=1.0,
                                            )
        start_game_button.on_click = self.start_game_click
        self.box_layout.add(start_game_button)

        # если нажать заработает метод records_click
        records_button = UITextureButton(text='Рекорды',
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0,
                                         )
        records_button.on_click = self.records_click
        self.box_layout.add(records_button)

        # если нажать заработает метод exit_click
        exit_button = UITextureButton(text='Выход',
                                      texture=texture_normal,
                                      texture_hovered=texture_hovered,
                                      texture_pressed=texture_pressed,
                                      scale=1.0,
                                      )
        exit_button.on_click = self.exit_click
        self.box_layout.add(exit_button)

    # запускает игру
    def start_game_click(self, event):
        self.game_view = GameView(self)
        self.window.show_view(self.game_view)

    # выходит с игры
    def exit_click(self, event):
        arcade.exit()

    # сохраненные рекорды игрока
    def records_click(self, event):
        # подключить к БД
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()
