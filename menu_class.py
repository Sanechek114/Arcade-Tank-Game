import arcade
from arcade.gui import (UITextureButton, UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIDropdown)

from game_view import GameView


# это для цвета кнопок если что
def get_color_tex(color):
    return arcade.make_soft_square_texture(60, color, outer_alpha=255)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN

        self.colors = ['red', 'blue', 'green', 'yellow']
        self.all_maps = ["1 карта", "2 карта", "3 карта", "4 карта"]

        with open("progress.txt", "r", encoding="utf8") as file:
            self.count = int(file.read().strip())

        self.available_maps = self.all_maps[:self.count]

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

        label = UILabel(text="Танчики",
                        font_size=60,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        start_game_button = UITextureButton(text='Начать игру',
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=1.0,
                                            )
        start_game_button.on_click = lambda event: self.start_game_click(event, self.colors[0])
        self.box_layout.add(start_game_button)

        records_button = UITextureButton(text='Рекорды',
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0,
                                         )
        records_button.on_click = self.records_click
        self.box_layout.add(records_button)

        color_row = UIBoxLayout(vertical=False, space_between=10)

        red_button = UITextureButton(text="", width=60, height=50,
                                     texture=get_color_tex(arcade.color.RED),
                                     texture_hovered=get_color_tex(arcade.color.DARK_RED))
        red_button.on_click = lambda event: self.start_game_click(event, self.colors[0])
        color_row.add(red_button)

        blue_button = UITextureButton(text="", width=60, height=50,
                                      texture=get_color_tex(arcade.color.BLUE),
                                      texture_hovered=get_color_tex(arcade.color.DARK_BLUE))
        blue_button.on_click = lambda event: self.start_game_click(event, self.colors[1])
        color_row.add(blue_button)

        green_button = UITextureButton(text="", width=60, height=50,
                                       texture=get_color_tex(arcade.color.GREEN),
                                       texture_hovered=get_color_tex(arcade.color.DARK_PASTEL_GREEN))
        green_button.on_click = lambda event: self.start_game_click(event, self.colors[2])
        color_row.add(green_button)

        yellow_button = UITextureButton(text="", width=60, height=50,
                                        texture=get_color_tex(arcade.color.YELLOW),
                                        texture_hovered=get_color_tex(arcade.color.GOLD))
        yellow_button.on_click = lambda event: self.start_game_click(event, self.colors[3])
        color_row.add(yellow_button)

        self.box_layout.add(color_row)

        self.dropdown = UIDropdown(
            default=self.available_maps[0],
            options=self.available_maps,
            width=200,
            height=30
        )
        self.box_layout.add(self.dropdown)

        exit_button = UITextureButton(text='Выход',
                                      texture=texture_normal,
                                      texture_hovered=texture_hovered,
                                      texture_pressed=texture_pressed,
                                      scale=1.0,
                                      )
        exit_button.on_click = self.exit_click
        self.box_layout.add(exit_button)

    def start_game_click(self, event, color='red'):
        select_map = self.dropdown.value
        self.game_view = GameView(self, color, select_map)
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
