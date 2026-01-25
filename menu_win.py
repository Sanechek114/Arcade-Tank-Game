import arcade
from arcade.gui import (UIManager, UIAnchorLayout, UIBoxLayout, UILabel)
from config import SCALE


class WinView(arcade.View):
    def __init__(self, game_view, menu, color, level, time):
        super().__init__()
        self.game_view = game_view
        self.menu = menu
        self.time_passed = 0
        self.text = 5
        self.color = color
        self.textXY = self.game_view.player.hull.position
        self.time = round(time, 2)

        with open('records.txt', 'a', ) as f:
            f.write(f"color: {self.color}, level: {level}, time: {self.time}\n")

        self.data = {}
        with open('progress.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(': ')
                    self.data[key] = int(value)

        levels = self.data[color]
        self.data[color] = min(4, (max([level + 1, levels])))
        with open('progress.txt', 'w') as f:
            for key, value in self.data.items():
                f.write(f"{key}: {value}\n")


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
        label = UILabel(text="ВЫ ВЫИГРАЛИ!",
                         font_size=30,
                         text_color=arcade.color.GREEN,
                         width=200,
                         align="center")
        self.box_layout.add(label)
        label2 = UILabel(text=f"За {self.time} секунд!",
                         font_size=30,
                         text_color=arcade.color.GREEN,
                         width=200,
                         align="center")
        self.box_layout.add(label2)
        label3 = UILabel(text="НАЖМИТЕ НА ПРОБЕЛ, ЧТОБЫ ПРОПУСТИТЬ",
                         font_size=30,
                         text_color=arcade.color.GREEN,
                         width=200,
                         align="center")
        self.box_layout.add(label3)
        self.label4 = UILabel(text="",
                         font_size=40,
                         text_color=arcade.color.RED,
                         width=200,
                         align="center")
        self.box_layout.add(self.label4)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.main_menu_button_click(None)

    def main_menu_button_click(self, event):
        self.menu.__init__()
        self.window.show_view(self.menu)

    def on_update(self, delta_time):
        self.time_passed += delta_time
        if self.time_passed >= 1 and self.text != 0:  # каждую 1 секунду
            self.text -= 1
            self.time_passed = 0
        if self.text == 0:
            self.main_menu_button_click(None)
        self.label4.text = self.text


class MyGUIWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
