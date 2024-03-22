import arcade
#Room class creates the room objects for the Clue game
#Attributes are name of room, whether it has secret passage, and what its entrance coordinates are
room_xs = { "study": 112, "hall": 385, "lounge": 657, "clue-room": 370}
room_ys = { "study": 703, "hall": 655, "lounge": 670, "clue-room": 402 }
class Room(arcade.Sprite):
    def __init__(self, name, passage_room, entrance_coordinates, fileName, scale):
        super().__init__(filename = fileName, scale = scale)
        self.name = name
        self.passage_room = passage_room
        self.entrance_coordinates = entrance_coordinates
        self.center_x = room_xs[name]
        self.center_y = room_ys[name]
        
    
#should there be a has_player variable?