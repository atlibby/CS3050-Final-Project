import arcade

# show the inventory of the player
class InventoryMenu(arcade.View):
    def __init__(self, game_view, hand):
        super().__init__()
        self.game_view = game_view
        self.hand = hand
        
        for item in hand:
            print(item)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

    def on_key_press(self, key, modifiers):
         self.window.show_view(self.game_view)
