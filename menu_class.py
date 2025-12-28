import arcade

from pyglet.graphics import Batch


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN  # Фон для меню

        self.batch = Batch()
        self.main_text = arcade.Text("Главное Меню", self.window.width / 2, self.window.height / 2 + 50,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView()  # Создаём игровой вид
            self.window.show_view(game_view)  # Переключаем

window = arcade.Window(800, 600, "")
menu_view = MenuView()
window.show_view(menu_view)
arcade.run()