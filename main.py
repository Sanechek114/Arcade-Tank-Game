from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
import arcade
from menu_class import MenuView

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
window.set_update_rate(1 / 600)
menu_view = MenuView()
window.show_view(menu_view)
arcade.run()
