from game_managment.entities import load_units, load_equipment, load_locations
from utils.helpers import can_move_to_location

units_data = load_units('data/units.json')
equipment_data = load_equipment('data/equipment.json')
locations_data = load_locations('data/locations.json')

class Player:
    def __init__(self, player_name, unit_id, start_location_id, units, locations, items):
        self.user_name = player_name
        self.unit = units[int(unit_id) - 1]
        self.items = items
        self.location = locations[start_location_id]
        self.inventory = []
        self.inventory_weight = 0

    def take_item(self):
        item_id = self.location.location_item_id
        item = self.items[int(item_id) - 1]
        if self.inventory_weight + item.weight <= self.unit.weight:
            self.inventory.append(item)
            self.inventory_weight += item.weight
        else:
            print("Вы не можете взять этот предмет!")

    def throw_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.inventory_weight -= item.weight
        else:
            print("У вас нет этого предмета в инвентаре!")

    def get_inventory_names(self):
        return [item.name for item in self.inventory]

    def change_location(self, new_location_id):
        if can_move_to_location(self, new_location_id):
            self.location = locations_data[int(new_location_id) - 1]
            print(f"{self.user_name} переместился в {self.location.name}")
        else:
            print("Невозможно переместиться в эту локацию!")