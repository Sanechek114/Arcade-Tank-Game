import arcade
from arcade.gui import (UITextureButton, UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIDropdown)

from game_view import GameView


# это для цвета кнопок если что
def get_color_tex(color, alpha=255):
    return arcade.make_soft_square_texture(60, color, center_alpha=alpha, outer_alpha=alpha)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.SMOKY_BLACK
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.all_maps = ["1 карта", "2 карта", "3 карта", "4 карта"]
        self.color = 'red'

        self.data = {}
        with open('progress.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(': ')
                    self.data[key] = int(value)
        self.turret = 1

        font = arcade.load_font('assets/south_park.ttf')
        self.customfont = 'South Park EXT'
        self.style = {"normal": UITextureButton.UIStyle(font_name=self.customfont, font_size=20),
                      "press": UITextureButton.UIStyle(font_name=self.customfont, font_size=20),
                      "hover": UITextureButton.UIStyle(font_name=self.customfont, font_size=20),
                      "pressed": UITextureButton.UIStyle(font_name=self.customfont, font_size=20)}

        self.available_maps = self.all_maps[:self.data[self.color]]

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
                        font_name=self.customfont,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        start_game_button = UITextureButton(text='Начать игру',
                                            style=self.style,
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=1.0
                                            )

        start_game_button.on_click = lambda event: self.start_game_click(event)
        self.box_layout.add(start_game_button)

        records_button = UITextureButton(text='Рекорды',
                                         style=self.style,
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0
                                         )
        records_button.on_click = self.records_click
        self.box_layout.add(records_button)

        # Кнопки выбора цвета

        color_row = UIBoxLayout(vertical=False, space_between=10)

        red_button = UITextureButton(text="", width=40, height=40,
                                     texture=get_color_tex(arcade.color.RED),
                                     texture_hovered=get_color_tex(arcade.color.DARK_RED))
        red_button.on_click = lambda event: self.change_color_click(event, self.colors[0])
        color_row.add(red_button)

        blue_button = UITextureButton(text="", width=40, height=40,
                                      texture=get_color_tex(arcade.color.BLUE),
                                      texture_hovered=get_color_tex(arcade.color.DARK_BLUE))
        blue_button.on_click = lambda event: self.change_color_click(event, self.colors[1])
        color_row.add(blue_button)

        green_button = UITextureButton(text="", width=40, height=40,
                                       texture=get_color_tex(arcade.color.GREEN),
                                       texture_hovered=get_color_tex(arcade.color.DARK_GREEN))
        green_button.on_click = lambda event: self.change_color_click(event, self.colors[2])
        color_row.add(green_button)

        yellow_button = UITextureButton(text="", width=40, height=40,
                                        texture=get_color_tex(arcade.color.YELLOW),
                                        texture_hovered=get_color_tex(arcade.color.DARK_YELLOW))
        yellow_button.on_click = lambda event: self.change_color_click(event, self.colors[3])
        color_row.add(yellow_button)

        self.box_layout.add(color_row)

        # Кнопки выбора пушки

        self.barel_row = UIBoxLayout(vertical=False, space_between=10)
        print(list(range(min(self.data[self.color], 3))))
        for i in range(min(self.data[self.color], 3)):
            print(i)
            barrel_button = UITextureButton(
                text="", scale=2,
                texture=arcade.load_texture(f"assets/sprites/barrels/tank{self.color.capitalize()}_barrel{i + 1}.png"))
            barrel_button.on_click = lambda event: self.change_turret_click(event, i + 1)
            self.barel_row.add(barrel_button)

        self.box_layout.add(self.barel_row)

        # Выбор карты

        self.dropdown = UIDropdown(
            default=self.available_maps[0],
            options=self.available_maps,
            width=190,
            height=30
        )
        self.box_layout.add(self.dropdown)

        self.exit_button = UITextureButton(
            text='Выход',
            style=self.style,
            texture=texture_normal,
            texture_hovered=texture_hovered,
            texture_pressed=texture_pressed,
            scale=1.0,
            )
        self.exit_button.on_click = self.exit_click
        self.box_layout.add(self.exit_button)

    def start_game_click(self, event):  # Начало игры
        select_map = self.all_maps.index(self.dropdown.value) + 1
        self.game_view = GameView(self, self.color, self.turret, select_map)
        self.window.show_view(self.game_view)

    def change_color_click(self, event, color):  # Смена цвета и Перезапуск некоторых виджетов
        self.color = color
        self.available_maps = self.all_maps[:self.data[self.color]]
        self.turret = 1

        self.box_layout.remove(self.dropdown)

        self.dropdown = UIDropdown(
            default=self.available_maps[0],
            options=self.available_maps,
            width=190,
            height=30
        )
        self.box_layout.add(self.dropdown)

        self.barel_row.clear()

        for i in range(min(self.data[self.color], 3)):
            barrel_button = UITextureButton(
                text="", scale=2,
                texture=arcade.load_texture(f"assets/sprites/barrels/tank{self.color.capitalize()}_barrel{i + 1}.png"))
            barrel_button.on_click = lambda event: self.change_turret_click(event, i + 1)
            self.barel_row.add(barrel_button)

        self.box_layout.remove(self.exit_button)
        self.box_layout.add(self.exit_button)

    def change_turret_click(self, event, turret):  # Сохранение пушки
        self.turret = turret
        print(turret)

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
