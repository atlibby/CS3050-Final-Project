#Room class creates the room objects for the Clue game
#Attributes are name of room, whether it has secret passage, and what its entrance coordinates are
class Room:
    def __init__(self, name, passage_room, entrance_coordinates):
        self.name = name
        self.passage_room = passage_room
        self.entrance_coordinates = entrance_coordinates
        pass
    
#should there be a has_player variable?