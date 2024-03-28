import arcade
#Room class creates the room objects for the Clue game
#Attributes are name of room, whether it has secret passage, and what its entrance coordinates are
room_xys = { "study": (112, 703), "hall": (385, 655), "lounge": (657, 670), "clue_room": (370, 402), "dining_room": (641, 369), "billiard_room": (97, 305), "kitchen": (673, 95), "conservatory": (97, 80), "ballroom": (385, 127), "library": (111, 494) }
class Room(arcade.Sprite):
    def __init__(self, name, passage_room, entrance_coordinates, fileName, scale):
        super().__init__(filename = fileName, scale = scale)
        self.name = name
        self.passage_room = passage_room
        self.entrance_coordinates = entrance_coordinates
        self.center_x = room_xys[name][0]
        self.center_y = room_xys[name][1]
        
    
#should there be a has_player variable?