from utils.helpers import generate_item


class Location:
    def __init__(self, location_id, locations, equipment):
        self.location_id = location_id
        self.name = locations[location_id]["name"]
        self.adjacent_locations = locations[location_id]["adjacent_locations"]
        self.distant_locations = locations[location_id]["distant_locations"]
        self.unavailable_locations = locations[location_id]["unavailable_locations"]
        self.equipment = equipment
        self.items = locations[location_id]["items"]
        self.location_items_by_player = {}  # ключ: player_name, значение: item_id
        self.current_players = []
        self.rules = locations[location_id].get("rules", None)

    def add_player(self, player):
        self.current_players.append(player)

    def delete_player(self, player):
        self.current_players.remove(player)

    def spawn_item_for_player(self, player):
        if player.user_name in self.location_items_by_player:
            return  # уже есть предмет для этого игрока
        item_id = generate_item(self.items)
        item_current_quantity = self.equipment[item_id].current_quantity
        while item_current_quantity == 0:
            item_id = generate_item(self.items)
            item_current_quantity = self.equipment[item_id].current_quantity
        self.location_items_by_player[player.user_name] = item_id
