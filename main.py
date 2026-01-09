from game_view import GameView
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
import arcade

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
window.set_update_rate(1 / 60)
menu_view = GameView()
window.show_view(menu_view)
arcade.run()
