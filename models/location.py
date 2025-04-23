from utils.helpers import spawn_item

class Location:
    def __init__(self, location_id, locations, equipment):
        self.location_id = location_id
        self.name = locations[location_id]["name"]
        self.adjacent_locations = locations[location_id]["adjacent_locations"]
        self.distant_locations = locations[location_id]["distant_locations"]
        self.unavailable_locations = locations[location_id]["unavailable_locations"]
        self.items = locations[location_id]["items"]
        self.location_item_id = spawn_item(self.items, equipment)
        self.current_players = []
        self.rules = locations[location_id].get("rules", None)

    def add_player(self, player):
        self.current_players.append(player)

    def delete_player(self, player):
        self.current_players.remove(player)